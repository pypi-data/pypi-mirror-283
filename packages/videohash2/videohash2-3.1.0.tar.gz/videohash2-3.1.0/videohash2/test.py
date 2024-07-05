from .videohash import VideoHash
import time

urls = ["https://t.me/bloodysx/29195",
        "https://t.me/bloodysx/28649",
        "https://t.me/bloodysx/28589",
        "https://t.me/bloodysx/28571",
        "https://t.me/bloodysx/28408",
        "https://t.me/bloodysx/27870",
        "https://t.me/bloodysx/27321",
        "https://t.me/bloodysx/27261",
        "https://t.me/bloodysx/29211"
        ]

start = time.time()

for url in urls:
    VideoHash(url=url, frame_interval=12)

end = time.time() - start
print(f"Completed in {end} seconds.")