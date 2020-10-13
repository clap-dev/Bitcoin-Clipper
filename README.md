# Bitcoin Clipper

A bitcoin clipper is a small piece of malware that detects when you have copied a bitcoin address, and will replace it with the a different address tricking you to send it to the wrong person.

## Usage
```bash
python Btc_Clipper.py
```

## How does it work?

Here's a quick rundown on how it works,

1. Every 1 second it checks to see if you have a valid bitcoin address copied to your clipboard via regex
2. When you have copied an address, it will check to see which is the closest matching address within a list, however, if there is no closest matching address it will default to the first index
3. It will then replace your copied address with a new one

## Why have you made this?

This is a quick demo on how malware is evolving in the *21st* century
