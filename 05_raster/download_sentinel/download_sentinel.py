from subprocess import call
import os
from osgeo import ogr
from datetime import datetime
import pandas as pd

#gsutil cp -r gs://gcp-public-data-sentinel-2/tiles/20/L/PQ/S2A_MSIL1C_20151230T142546_N0201_R010_T20LPQ_20151230T235521.SAFE ./
#https://krstn.eu/landsat-batch-download-from-google/


grid_sentinel = r'B:\monitoramento_kfw\arvore_processos\dev_2019_RO_PA\imgs\grid_sat.shp'


outfolder = r".\images"

startdate = '2019-01-01'
enddate = '2019-09-04'

tile_limit = 1

cloud_limit = 1
#sat = '8'

sort_columns = ['CLOUD_COVER', 'SENSING_TIME']
bands = [2,3,4,8]

update_index = False
#stDate = re.compile(r'201[6789][01]\d[0123]\d')
dirname = os.getcwd()
def download_sentinel(tilefuso,single_letter,double_letter,cloud_limit,tile_limit,startdate,enddate,sortColumns,outfolder,bands):
    file_name = r".\index\sentinel_index.pickle"
    if not os.path.isfile(file_name) or update_index == True:
        print('processing index')
        call("python process_index.py",shell=True)
        print('complete!')
    df = pd.read_pickle(file_name)
    tile_id = '{}_{}_{}'.format(tilefuso,single_letter,double_letter)
    start = datetime.strptime(startdate, '%Y-%m-%d')
    end = datetime.strptime(enddate, '%Y-%m-%d')
    select = df[(df['SENSING_TIME'] >= start) & (df['SENSING_TIME'] <= end)]
    select = select[(select['TILE_ID'] == tile_id)]
    select = select[select['CLOUD_COVER'] <= cloud_limit]
    select.sort_values(sortColumns)
    td_numb = 0
    out_tile_folder = os.path.join(outfolder,tile_id)
    call('mkdir {}'.format(out_tile_folder),shell=True)
    if len(select) != 0:
        #print products
        for i in select.index.values:            
            if td_numb >= tile_limit:
                break
            td_numb +=1
            print ('downloading scene number {} for this tile id'.format(td_numb))
            print select.at[i,'PRODUCT_ID']
            url = select.at[i,'BASE_URL'].strip()
            try:
                call('python ".\gsutil\gsutil.py" -m -q cp -r {} {}'.format(url,out_tile_folder),shell=True)
            except Exception as e:
                print(e)
                continue
            finally:
                print('download complete! \n')
    else:
        print('could not find any scene with that criteria')
    scenes = stack_sentinel(out_tile_folder,outfolder,bands)
    print scenes

def parse_gfilename(name):
    name = '_'.join(name.split('_')[-3:])
    return name

def parse_tile_info(name):
    tile = name.split('_')[0]
    date = name.split('_')[1]
    lis = [tile,date]
    return lis

def generate_band_names(basename,root,bands):
    band_paths = []
    for b in bands:
        b1 = basename+'_B0{}.jp2'.format(b)
        b1 = os.path.join(root,b1)
        band_paths.append(b1)
    return band_paths

def stack_sentinel(inpath,outpath,bands):
    for r,d,f in os.walk(inpath):
        #dateset = set()
        info = []
        folder = r.split('\\')[-1]
        if folder == 'IMG_DATA':
            band = f[0]
            info = parse_tile_info(band)
            if info:
                print(info[0])
                basename = info[0]+'_'+info[1]
                root = '\\'.join(r.split('\\')[1:])
                abspath = os.path.join(dirname,root)
                band_paths = generate_band_names(basename,abspath,bands)
                #print(band_paths)
                output = basename+'.tif'
                outputp = os.path.join(outpath,output)
                band_str = ' '.join(band_paths)
                call('gdal_merge -separate {} -o {}'.format(band_str,outputp),shell=True)
                return outputp
def main():
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(grid_sentinel, 0) # 0 means read-only. 1 means writeable
    layer = dataSource.GetLayer()   
    for feature in layer:
        tile = feature.GetField('tile_id')
        tile_fuso = tile[0:2]
        single_letter = tile[2:3]
        double_letter = tile[3:]
        print tile_fuso,single_letter,double_letter
        download_sentinel(tile_fuso,single_letter,double_letter,cloud_limit,tile_limit,startdate,enddate,sort_columns,outfolder,bands)

if __name__ == "__main__":
    main()