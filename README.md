# CryptoWall tooling / information
This repository contains scripts / snippets created during my analysis of CryptoWall throughout the years.

* cryptowall-post-decoder.py: allows you to decode the communication from infectees
  * Usage: *`cryptowall-post-decoder.py <request location/param> <request/response data>`*
  * Example:
```
       cryptowall-post-decoder.py vob9xevd95ej 37f51e98e2b5516638237800ff0cadab76e98521313a53555ee9d8575695ac0d80bc1335162dd6979b23fb5fb11443708ac8be5206
 
       {7|crypt19|4E0C0303057CD36249C03664F195D715|3|all=28}
```
* decompress-cryptolocker-clone-bundle.py: allows you to decompress the fileblob downloaded by the CryptoLocker clone CryptoWall samples
  * Usage: *`decompress-cryptolocker-clone-bundle.py <bundle filename> <directory for output>`*
  * Example:
```
       	decompress-cryptolocker-clone-bundle.py us_4.bin.out ./decomped_files*

		[+] Found new fileblob in container
			- Checksum:  0x8df196bc
			- Size:  1259
		[+] Found new fileblob in container
			- Checksum:  0x2c989a55
			- Size:  3272
		[+] Found new fileblob in container
			- Checksum:  0x90ae8cc
			- Size:  205
		[+] Found new fileblob in container
			- Checksum:  0xb7def142
			- Size:  2715
```