# dxomark-crawl
quickly crawl the mobile camera review from https://www.dxomark.com/


### Getting started
Just do:
```bash
git clone https://github.com/nightmello/dxomark-crawl.git
```

It uses requests and lxml to get all the information, so install them with:
```bash
pip install -r requirements.txt
```


### Use it
Now you can start using it:
```bash
python crawl.py
```

The results will be saved into output folder and 
[output/README.md](https://github.com/nightmello/dxomark-crawl/tree/master/output/README.md).


### Keep in mind
The [DXOMARK](https://www.dxomark.com/) website will be updated all the time.
If the webpage template is changed, just update the parser rules in the 
[``crawl.py``](https://github.com/nightmello/dxomark-crawl/blob/master/crawl.py#L26_L53).
