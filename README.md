# ptt_crawler
The crawler for PTT hot board and PTT ALLPOST, but it's still update.

### PTT ALLPOST

##### python3 ptt_all_post_v4.py -d 1 -o ~/output/path/file.txt

抓一個整天。 -d 1 是抓當下時間到當天凌晨， -d 2 代表抓昨天 00:00 ~ 23:59

> -d 抓取天數，int，範圍 1 ~ 7 （ 2 代表昨天，會抓到昨天到今天凌晨 00:00 ，完整一天 ）
> 
> -o 輸出的檔名路徑
> 

##### python3 ptt_all_post_v4.py -h 

> -h 提示
> 

------

##### python3 ptt_all_post_v3.py -d 1 -o ~/output/path/file.txt

由今天往前抓， -d 5 代表抓從今天到五天前的資料。

> -d 抓取天數，int，範圍 1 ~ 7 （ 1 代表今天，會抓到今天凌晨 00:00 ）
>
> -o 輸出的檔名路徑
>

##### python3 ptt_all_post_v3.py -h

> -h 提示
>

-------

### PTT HOT BOARD

抓取 熱門看板數據 ： 版標,人數...等

##### python3 ptt_hotboards_v1.py


##### Docker Image

透過 Docker 啟動爬蟲：

```
docker build -t ptt_crawler .
mkdir out
docker run -v `pwd`/out:/usr/src/app/out ptt_crawler
```
