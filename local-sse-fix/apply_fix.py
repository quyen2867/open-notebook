"""Apply a narrow runtime hotfix to the pinned, already-built Docker image."""

import hashlib
import json
from pathlib import Path


def verified(path, expected):
    file = Path(path)
    assert hashlib.sha256(file.read_bytes()).hexdigest() == expected, path
    return file, file.read_text()


def fallback_rewrites(rewrites):
    assert rewrites['beforeFiles'] == []
    assert rewrites['fallback'] == []
    assert len(rewrites['afterFiles']) == 1
    rule = rewrites['afterFiles'][0]
    assert rule['source'] == '/api/:path*'
    assert rule['destination'] == 'http://localhost:5055/api/:path*'
    rewrites['fallback'] = rewrites['afterFiles']
    rewrites['afterFiles'] = []


# Keep build metadata and standalone configuration consistent. No JS bundles
# change: the SSE Route Handler is already included in this pinned image.
file, text = verified('/app/frontend/.next/routes-manifest.json',
    '00ddae2a680757f3d616bede171b025d2d002a9109b423e0a3f40cc070ae2963')
manifest = json.loads(text)
fallback_rewrites(manifest['rewrites'])
file.write_text(json.dumps(manifest, indent=2) + '\n')

file, text = verified('/app/frontend/.next/required-server-files.json',
    '94da659d5c60046f4594171d7940513a241e013c752606a283a90d9f76e67639')
manifest = json.loads(text)
fallback_rewrites(manifest['config']['_originalRewrites'])
file.write_text(json.dumps(manifest, indent=2) + '\n')

file, text = verified('/app/frontend/server.js',
    '307a834958d34bbd22022c172faa65b4ff3a852aef3df7afd662b4f71adfeef8')
prefix = 'const nextConfig = '
lines = text.splitlines(keepends=True)
matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
assert len(matches) == 1
i = matches[0]
config = json.loads(lines[i][len(prefix):])
fallback_rewrites(config['_originalRewrites'])
lines[i] = prefix + json.dumps(config, separators=(',', ':')) + '\n'
file.write_text(''.join(lines))

# Also fix source configuration, so a future rebuild of this tree retains it.
file = Path('/app/frontend/next.config.ts')
text = file.read_text()
old = """    return [
      {
        source: '/api/:path*',
        destination: `${internalApiUrl}/api/:path*`,
      },
    ]"""
new = """    return {
      fallback: [
        {
          source: '/api/:path*',
          destination: `${internalApiUrl}/api/:path*`,
        },
      ],
    }"""
assert text.count(old) == 1
file.write_text(text.replace(old, new))

file, text = verified('/app/api/routers/source_chat.py',
    '7bcfc44fa3bd5a907f8ce6724ef7cad7b3fe05e672124d739464bf1f4b7de47c')
anchor = 'from api.routers._chat_shared import ('
assert text.count(anchor) == 1
text = text.replace(anchor,
    'from api.routers._sse_keepalive import stream_with_heartbeats\n\n' + anchor)
old = '''            stream_source_chat_response(
                session_id=full_session_id,
                source_id=full_source_id,
                message=request.message,
                model_override=model_override,
            ),'''
new = '''            stream_with_heartbeats(
                stream_source_chat_response(
                    session_id=full_session_id,
                    source_id=full_source_id,
                    message=request.message,
                    model_override=model_override,
                )
            ),'''
assert text.count(old) == 1
text = text.replace(old, new)
text = text.replace('"Cache-Control": "no-cache",',
                    '"Cache-Control": "no-cache, no-transform",')
compile(text, str(file), 'exec')
file.write_text(text)
print('Applied Source Chat SSE routing and heartbeat hotfix.')
