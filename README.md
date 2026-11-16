# ETOLEGKO — Download Speed Test

Downloads a URL 10 times in a row and prints the average request time,
total data downloaded and download speed.

## Usage

Requires Python 3.7+, no extra packages.

```sh
python3 speedtest.py 'https://images.unsplash.com/photo-1628921755231-0371004cc853?q=80'
```

Use `-n N` to change the number of requests. Keep the URL in quotes.

## Units

- Size: **MB** (1 MB = 1,000,000 bytes)
- Speed: **MB/s** (total MB ÷ total seconds)
