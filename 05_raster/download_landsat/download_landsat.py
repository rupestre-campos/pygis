
from subprocess import call
from osgeo import ogr,gdal
import os
from datetime import datetime
import pandas as pd
import sys

#download gsutil
# https://drive.google.com/open?id=1mXZvVtBJCtgMRmm0pK_X8ihbrHRrH4zj
# and filtered dataframe stored in pickle
# https://drive.google.com/open?id=1gCn_ax6QnrieZUXnjdXLGguyS8kYtYQF


satAtrDic = {'sat':'LANDSAT_5','tile_id':['225/061','224/061']}
outfolder = r"B:\curso_python_gis\data\raster"

databaseUser = "***"
databasePW = "****"

databaseServer = "****"
databaseName = "equipe_geo"

tier = 'T1'
startdate = '2008-07-23'
enddate = '2009-01-01'

tile_limit = 1

cloud_limit = 50
sortColumns = ['CLOUD_COVER']
bands = [1,2,3,4,5]#,'QA']





def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def createAtrFilterfromDic(dic):
    atrList = []
    for atr,values in dic.iteritems():
        if type(values) != list:
            values = [values]
        filtList = []
        filt = ''
        for i in range(len(values)):
            if str(values[i]).startswith('LANDSAT'):
                values[i] = 'LANDSAT'
            elif str(values[i]).startswith('SENTINEL'):
                values[i] = 'SENTINEL'

            filt = "{} = '{}'".format(atr,values[i])
            filtList.append(filt)
        filt = "({})".format(' OR '.join(filtList))
        atrList.append(filt)
    return ' AND '.join(atrList)

def getEpsgFromFuse(fuse,epsg):
    #fuses = [18,19,20,21,22,23,24,25]
    try:
        fuse = int(fuse)
    except Exception:
        print type(fuse)
        print fuse
        print 'is this correct?'
    epsg_dic = {}
    if epsg == 4326:
        for fuso in range(18,26):
            epsgS = int('327{}'.format(fuso))
            epsgN = int('326{}'.format(fuso))
            epsg_dic[-fuso] = epsgS
            epsg_dic[fuso] = epsgN
    elif epsg == 4674:
        codN = 72
        codS = 78
        for fuso in range(18,26):
            epsgS = int('319{}'.format(codS))
            epsgN = int('319{}'.format(codN))
            epsg_dic[-fuso] = epsgS
            epsg_dic[fuso] = epsgN
            codN += 1
            codS += 1
    return epsg_dic[fuse]

def parseTileInfo(name):
    tile = name.split('_')[2]
    date = name.split('_')[3]
    info = [tile,date]
    return info

def generate_band_names(bands,basename,root):
    bandsp = []
    for band in bands:
        b = basename+'_B{}.TIF'.format(band)
        bp = os.path.join(root,b)
        bandsp.append(bp)
    return ' '.join(bandsp)

def stack_landsat(tilefuso,bands,inpath,path,row):
    infoDic = {}
    for r,d,f in os.walk(inpath):
        if r == inpath:
            continue
        info = []
        folder = r.split('\\')[-1]
        #info = parseTileInfo(folder)
        if folder in infoDic:
            continue
        else:
            print '\nstacking your scenes'
            #print 'path/row: {}'.format(info[0])
            #basename = info[0]+'_'+info[1]
            bandstr = generate_band_names(bands,folder,r)
            output = folder+'np.tif'
            outputp = os.path.join(inpath,output)
            call('gdal_merge -separate {} -o {}'.format(bandstr,outputp),shell=True)
            epsg = getEpsgFromFuse(tilefuso,4674)
            output = folder+'.tif'
            outputp2 = os.path.join(inpath,output)
            print 'reprojecting to EPSG:{}'.format(epsg)
            call('gdalwarp --config GDAL_CACHEMAX 12000 -wm 512 -wo "NUM_THREADS=ALL_CPUS" -t_srs EPSG:{} {} {}'.format(epsg,outputp,outputp2))
            call('rmdir /S /Q {}'.format(r),shell=True)
            call('del /Q {}'.format(outputp),shell=True)
            #infoDic[folder] = {'path':outputp2,'tile_id':info[0],'date':info[1]}
    else:
        return 0

def downloadScenes(sat,tilefuso,path,row,cloud_limit,tier,tile_limit,startdate,enddate,sortColumns,outfolder,bands):
    script_path = get_script_path()
    pickle = os.path.join(script_path,"landsat_filtered_dataframev3.pickle")
    df = pd.read_pickle(pickle)
    tile_id = '{}_{}'.format(int(path),int(row))
    start = datetime.strptime(startdate, '%Y-%m-%d')
    end = datetime.strptime(enddate, '%Y-%m-%d')
    #dateMask = (df['SENSING_TIME'] >= start) & (df['SENSING_TIME'] <= end)
    select = df[(df['SENSING_TIME'] >= start) & (df['SENSING_TIME'] <= end)]
    select = select[(select['TILE_ID'] == tile_id) & (select['SAT'] == sat)]
    #select = select[(select['COLLECTION_NUMBER'] == '01')]#& (select['COLLECTION_CATEGORY'] == tier)]
    select = select[select['CLOUD_COVER'] <= cloud_limit]
    select.sort_values(sortColumns)
    
    gsutil_path = os.path.join(script_path,'gsutil','gsutil.py')
    td_numb = 0
    if len(select) != 0:
        #print products
        for i in select.index.values:            
            if td_numb >= tile_limit:
                continue
            td_numb +=1
            print ('downloading scene number {} for this tile id'.format(td_numb))
            print select.at[i,'SCENE_ID']
            url = select.at[i,'BASE_URL'].strip()

            try:
                call('python {} -m -q cp -r {} {}'.format(gsutil_path,url,outfolder),shell=True)
                #api.download(image,directory_path=outfolder)
            except Exception as e:
                print(e)
                continue
            finally:
                print('download complete! \n')
        #print max_cloud_p

        # download all results from the search
        #api.download_all(products)
    else:
        print('could not find any scene with that criteria')

    scenes = stack_landsat(tilefuso,bands,outfolder,path,row)
    print '\n scenes dictionary'
    print scenes
    #createFP(scenes,outfolder)
    return scenes


def main():
    #sat = satAtrDic['sat']
    #path = tileId.split("/")[0]
    #row = tileId.split("/")[-1]
    connString = "PG: host=%s dbname=%s user=%s password=%s" %(databaseServer,databaseName,databaseUser,databasePW)

    conn = ogr.Open(connString)
    satLay = conn.GetLayer('python_gis.grid_sat')
    satLay.SetAttributeFilter(createAtrFilterfromDic(satAtrDic))
    for tile in satLay:
        tileId = tile.GetField("tile_id")
        tilefuso = tile.GetField("fuso")
        print tile.GetField("sat"),tile.GetField("tile_id")
        path = tileId.split("/")[0]
        row = tileId.split("/")[-1]
        #time2 = time.time()
        #timeExec(time1,time2,"","")
        sat = satAtrDic['sat']
        #try:
        scenes = downloadScenes(sat,tilefuso,path,row,cloud_limit,tier,tile_limit,startdate,enddate,sortColumns,outfolder,bands)
        #except Exception:
        #    continue
        #time3 = time.time()
        #timeExec(time2,time3,'download and process scenes', '')

if __name__ == "__main__":
    main()