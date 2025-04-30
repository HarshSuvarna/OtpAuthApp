import streamlink
streams = streamlink.streams("hls://devstreaming-cdn.apple.com/videos/streaming/examples/bipbop_4x3/bipbop_4x3_variant.m3u8")
print(streams)