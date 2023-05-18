Proteomes
=========

There are a couple scripts and files here to associate protein names with gene
names.

### Worm

Wormpep uses the protein name as the main identifier. The protein is named
after the coding transcript name. The additional .1 after the name of a
transcript is an alternative splice that doesn't affect the CDS. 

```
# name, pid, tid, gid
Y74C9A.3        CE28146 Y74C9A.3.1      WBGene00022277
Y74C9A.2a       CE24660 Y74C9A.2a.1     WBGene00022276
Y74C9A.2a       CE24660 Y74C9A.2a.3     WBGene00022276
Y74C9A.2a       CE24660 Y74C9A.2a.2     WBGene00022276
```

### Fly

Flypep uses the FBpp number as the main identifier. The protein is named after
the gene name when possible.

```
# name, pid, tid, gid
Nep3-PA FBpp0070000     FBtr0070000     FBgn0031081
Nep3-PB FBpp0300206     FBtr0307554     FBgn0031081
Nep3-PC FBpp0300207     FBtr0307555     FBgn0031081
CG9570-PA       FBpp0070001     FBtr0070002     FBgn0031085
Or19b-PA        FBpp0070002     FBtr0070003     FBgn0062565
CG15322-PB      FBpp0290784     FBtr0301569     FBgn0031088
```

