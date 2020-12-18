#!/usr/bin/env python3
# coding=utf-8
import httpx
import pandas as pd
from typing import Tuple, Type
import datetime
from pandas.tseries.offsets import BDay
import pickle
import asyncio
from io import StringIO
from pathlib import Path
from norway import Norway
import os

# >  R O A D M A P <
# 0. get code on github                                 [ OK ]
# 1. get heroku dyno up (hobby)                         [ OK ]
# 2. get C custom queries up                            [ OK ]
# 2. get ENV storage key running                        [ OK ]
# 2  get fylker working                                 [ OK ]
# 2. create jinjatemplate for error messages            [    ]
# 2. implement error message template redirects         [    ]
# 3. get https up and enable https only middleware      [ OK ]
# 4. get custom query submission up                     [    ]
# 5. get subdomains working                             [ OK ]
# 6. get languages working (gettext or equiv)           [    ]
# 7. various TODOs (optimization) below                 [    ]
# 8 . add postnummer to search keys                     [ OK ]

# TODO
# async httpx fetch loop
# => use httpx's Client setup to re-use TCP

# TODO
# async query loop
# Could be huge savings

# TODO
# async web form POST / return data interaction (interesting turn)

# TODO
# use try/except/else with ELSE containing the code
# that will run if try succeeds.
# minimize code in try block. Use finally block for cleanup

# TODO
# Currently we are hybriding between csv, pandas and python dictionaries
# How about we stick to pandas and dataframes?
# The h5 storage can store the CURRENT_DATA as a frame
# This means we only need logic to determine (when refresh_data is run)
# whether the data already exists in the CURRENT_DATA frame.

class Session():
    """ Necessary settings for running through app:app """
    def __init__(self):
        self.max_data_age = 14
        self.age = 14
        self.store = self.get_store_target() # on-disk store
        self.is_setup = True
        self.FHI = None # pointer to FHI source object
        self.norge = None  # pointer to norge data object
        self.custom = self.custom_queries()
        self.custom_queries = self.custom
        self.list_custom = list(self.custom.keys())

    def get_store_target(self) -> str:
        """ heroky config var for storage file name """
        try:
            store_in = os.environ["cloud_storage_loc"]
        except:
            store_in = "storage.pkl"
        finally:
            return store_in

    def custom_queries(self) -> dict:
        """ key store for custom queries we call with GET """
        _cq = {
                "vvhf": {
                        "title":    "Vestre Viken Helseforetak",
                        "subtitle": "Gjeldende tall for alle kommuner under VVHF",
                        "created":  "2020-11-18",
                        "list":     ('Asker','Bærum','Drammen','Flå','Flesberg',
                                    'Gol','Hemsedal','Hol','Hole','Jevnaker',
                                    'Kongsberg','Krødsherad','Lier','Modum',
                                    'Nesbyen','Nore og Uvdal','Øvre Eiker',
                                    'Ringerike','Rollag','Sigdal', 'Ål')
                        },
                "vvhfsyk": {
                        "title":    "Vestre Viken HF",
                        "subtitle": "VVHF kommuner etter sykehus",
                        "created":  "2020-11-18",
                        "list":     ()  # sykehusregionene i tur og orden
                },
                "ringsyk": {
                        "title":    "Ringerike Sykehus",
                        "subtitle": "Vestre Viken Helseforetak",
                        "created":  "2020-11-18",
                        "list":     ('Flå', 'Gol', 'Hemsedal', 'Hol', 'Hole',
                                     'Jevnaker', 'Krødsherad', 'Modum',
                                     'Nesbyen', 'Ringerike', 'Sigdal', 'Ål')
                        },
                "bersyk": {
                        "title":    "Bærum Sykehus",
                        "subtitle": "Vestre Viken Helseforetak",
                        "created":  "2020-11-18",
                        "list":     ('Asker', 'Bærum')
                        },
                "dramsyk": {
                        "title":    "Drammen Sykehus",
                        "subtitle": "Vestre Viken Helseforetak",
                        "created":  "2020-11-18",
                        "list":     ('Drammen', 'Lier')
                        },
                "kongsyk": {
                        "title":    "Kongsberg Sykehus",
                        "subtitle": "Vestre Viken Helseforetak",
                        "created":  "2020-11-20",
                        "list":     ('Flesberg', 'Kongsberg', 'Nore og Uvdal',
                                     'Rollag', 'Øvre Eiker')
                        },
                "E6": {
                        "title":    "Europavei 6 sørover",
                        "subtitle": "Landets lengste veistrekning 2578 km",
                        "created":  "2020-11-18",
                        "list":     ('Sør-Varanger','Nesseby','Tana','Karasjok',
                                    'Porsanger','Hammerfest','Alta','Kvænangen',
                                    'Nordreisa','Kåfjord','Storfjord',
                                    'Balsfjord','Målselv','Bardu','Lavangen',
                                    'Gratangen','Narvik','Hamarøy','Sørfold',
                                    'Fauske','Saltdal','Rana','Hemnes','Vefsn',
                                    'Grane','Namsskogan','Grong','Snåsa',
                                    'Steinkjer','Inderøy','Verdal','Levanger',
                                    'Stjørdal','Malvik','Trondheim','Melhus',
                                    'Midtre Gauldal','Rennebu','Oppdal','Dovre',
                                    'Sel','Nord-Fron','Sør-Fron','Ringebu',
                                    'Øyer','Lillehammer','Gjøvik','Ringsaker',
                                    'Hamar','Stange','Eidsvoll','Ullensaker',
                                    'Lillestrøm','Lørenskog','Oslo','Ås',
                                    'Frogn','Vestby','Moss','Råde','Sarpsborg',
                                    'Fredrikstad','Halden')
                },
                "byer": {
                    "title":    "Byer i Norge",
                    "subtitle": "Tilstanden i norske by-kommuner",
                    "created":  "2020-12-09",
                    "list":     ('Alta', 'Arendal', 'Bergen', 'Bodø', 'Drammen',
                                'Elverum', 'Farsund', 'Fauske', 'Flekkefjord',
                                'Fredrikstad', 'Gjøvik', 'Grimstad', 'Halden',
                                'Hamar','Hammerfest','Harstad','Haugesund',
                                'Holmestrand', 'Horten', 'Kongsberg',
                                'Kongsvinger', 'Kragerø', 'Kristiansand',
                                'Kristiansund', 'Larvik', 'Levanger',
                                'Lillehammer', 'Lillesand', 'Lillestrøm',
                                'Lyngdal', 'Molde', 'Moss', 'Namsos', 'Narvik',
                                'Notodden', 'Oslo', 'Porsgrunn', 'Risør',
                                'Røros', 'Sandefjord', 'Sandnes', 'Sarpsborg',
                                'Sauda', 'Skien', 'Sortland', 'Stavanger',
                                'Steinkjer', 'Stord', 'Tromsø', 'Trondheim',
                                'Tvedestrand', 'Tønsberg', 'Vadsø', 'Vardø',
                                'Ålesund')
                }
        }
        return _cq

class Folkehelseinstituttet():
    """
    Holds URL and stuff to the data from Folkehelseinstituttet
    """

    def __init__(self, store:str):
        self.git = "https://raw.githubusercontent.com"
        self.fhi = "folkehelseinstituttet"
        self.surveillance_data = "surveillance_data/master/covid19/"
        self.name = self.fhi.capitalize()
        #self.store = HDFStore('storage.h5') # on-disk store
        self.store = store
        self.book = {}    # dictionary of raw data
        self.current = {} # today's processed data
        self.resize_db = False
        self.today = datetime.datetime.now().isoformat().split(sep="T")[0]
        self.fresh = None

    def msis_file(self, data_date:str) -> str:
        """ returns FHI file name from input string """
        return f"data_covid19_msis_by_location_{data_date}.csv"

    def msis_url(self, get_date:str) -> str:
        """ returns FHI csv file string from input date string """
        self.msis = self.msis_file(get_date)
        return f"{self.git}/{self.fhi}/{self.surveillance_data}/{self.msis}"


async def dl_csv_data(msis_url: str) -> Type[httpx.Response]:
    """ Downloads msis data as csv """
    async with httpx.AsyncClient() as client:
        data_file = await client.get(msis_url)
    return data_file


async def db_refresh(
                 date: str,
                 big_book: dict,
                 query_object: Type[Folkehelseinstituttet]
                 ):
    """
    depends on FHI object created in main() or supply one yourself
    downloads CSV files for dates in list we don't already have locally
    and appends to our local "big book" hash table data store
    """
    # Get it online
    msis_url = query_object.msis_url(date)
    data_file = await dl_csv_data(msis_url)
    #data_file, get_status = dl_csv_data(msis_url)
    if data_file.status_code == 200:
        print(f" -> msis for {date}")
        df = pd.read_csv(StringIO(data_file.content.decode('utf-8')))
        for _, row in df.iterrows():
            if row.granularity_geo == 'municip':
                k = row.location_name
                kid = row.location_code
                if kid[:7] == 'municip':
                    kid = kid[7:]
                else:
                    continue # drop record
                dest = kid
                n, po, pro = row.n, row['pop'], row.pr100000
                big_book['ro'][date][kid] = (n, po, pro, k)
            elif row.granularity_geo == 'nation':
                n, po, pro = row.n, row['pop'], row.pr100000
                big_book['ro'][date]['0000'] =  (n, po, pro, 'Norge')
    else:
        print(f" xx msis for {date} skipped:{data_file.status_code}")


async def refresh_data(
                 dates: list,
                 big_book: dict,
                 storage: str,
                 query_object: Type[Folkehelseinstituttet]
                 ):
    """(n, po, pro, k)
    depends on FHI object created in main() or supply one yourself
    downloads CSV files for dates in list we don't already have locally
    and appends to our local "big book" hash table data store
    """
    for date in dates:
        if date in big_book['ro'].keys():
            continue
        else:
            try:
                big_book['ro'][date]
            except KeyError:
                big_book['ro'][date] = {}
            await db_refresh(date, big_book, query_object)

    save_to_file(big_book, storage)

#     for date in dates:
#         # check if data is in store already
#         if date in big_book['ro'].keys():
#             continue
#         else:
#             # setup ro sub dict
#             try:
#                 big_book['ro'][date]
#             except KeyError:
#                 big_book['ro'][date] = {}
#
#             # Get it online
#             msis_url = query_object.msis_url(date)
#             try:
#                 async with httpx.AsyncClient() as client:
#                     data_file = await client.get(msis_url) # headers={"Range": "bytes=0-100"}
#                 if data_file.status_code == 200:
#                     print(f" -> msis for {date}")
#                     #dat = data_file.content
#                     #df = await pd.read_csv(print(dat))
#                     df = pd.read_csv(StringIO(data_file.content.decode('utf-8')))
#
#
#                     # df = await pd.read_csv(msis_url)
# #                           for _, row in df.where(granularity_geo="municip").iterrows():
# #                           df = df.where(granularity_geo="municip").iterrows():
#                     for _, row in df.iterrows():
#                         if row.granularity_geo == 'municip':
#                             k = row.location_name
#                             kid = row.location_code
#                             if kid[:7] == 'municip':
#                                 kid = kid[7:]
#                             else:
#                                 continue # drop record
#                             dest = kid
#                             n, po, pro = row.n, row['pop'], row.pr100000
#                             big_book['ro'][date][kid] = (n, po, pro, k)
#                         elif row.granularity_geo == 'nation':
#                             n, po, pro = row.n, row['pop'], row.pr100000
#                             big_book['ro'][date]['0000'] =  (n, po, pro, 'Norge')
#                 else:
#                     continue
#             except:
#                 # page not found (source not released yet)
#                 continue
#
#     # dump to disk
#     save_to_file(big_book, storage)

#def recompress_database(storage: HDFStore):
#    """ periodically re-build h5 file (reduce size) """
#    pass # TBD
#    # See: https://github.com/jackdotwa/python-concepts/blob/master/hdf5/reclaiming_space.ipynb

def save_to_file(input:dict, storage:str):
    """ saves input dict to storage file """
    with open(storage, 'wb') as f:
        pickle.dump(input, f, pickle.HIGHEST_PROTOCOL)
    f.close()

def load_from_file(storage:str) -> dict:
    """ loads input storage file into a dict """
    if Path(storage).is_file():
        with open(storage, 'rb') as f:
            dictus = pickle.load(f)
        f.close()
    else:
        dictus = {}
    return dictus

def clear_data(dates:list, max_age: int, storage: str) -> bool:
    """ Clears stale data (older than MAX_DATA_AGE by 3 days) """

    # TBD This must be updated to use new pickle scheme
    pass
    remove_older_than = max_age + 3
    did_something = False
    #for key in storage.keys():
    #    date = key[1:]
    #    if date in dates:
    #        continue
    #    else:
    #        real_date = datetime.datetime.fromisoformat(date)
    #        if real_date < remove_older_than:
    #            storage.remove(date)
    #            did_something = True

    return did_something


def read_data(
              selection: list,
              storage: str
              ) -> dict:
    """ read local binary pickle into trimmed dict """
    # source from disk
    store = load_from_file(storage)

    # TODO optimization
    # Consider deep copy instead and just remove() keys not in selection...?
    # Wait: cloud storage unstable

    # target dict
    kom_dat = {}
    kom_dat['ro'] = {}
    target = kom_dat['ro']

    try:
        store['ro']
        for date in store['ro'].keys():
            if date in selection:
                for k, v in store['ro'][date].items():
                    enn, population, *pro100k = v
                    values = (enn, population, pro100k[0])
                    try:
                        target[date]
                    except:
                        target[date] = {}

                    try:
                        target[date][k]
                    except:
                        target[date][k] = {}

                    # saves 'values' tuple: (n, population, pro100k)
                    target[date][k] = values

        # Get national level, if possible
        # TBD clean up this and replace with deep copy
        try:
            target['0000'] = {}
            for k,v in store['0000'].items(): target['0000'][k] = v
        except:
            pass

        try:
            kom_dat['ro']
        except:
            print("read_data: No 'ro' in database?")

    except KeyError:
        pass # no data yet

    return kom_dat


# def read_data_obsolete(
#               dates:list,
#               storage: str # was HDFStore
#               ) -> dict:
#     """ Read local h5 storage into dictionary """
#     kom_dat = {}
#     kom_dat['ro'] = {}
#     target = kom_dat['ro']
#
#     # Note keys are iso date strings (prefixed with h5 "/")
#     for key in storage.keys():
#         print(f"key={key}")
#         date = key[1:] # e.g. 2020-11-09
#         if date in dates:
#             print(f"date={date}")
#             for _, row in storage[key].iterrows():
#                 k = row.location_name
#                 enn = row.n
#                 population = row['pop']
#                 pro100k = row.pr100000
#                 values = (enn, population, pro100k)
#                 print(f"k={k}, values={values}")
#
#                 try:
#                     target[date]
#                 except KeyError:
#                     target[date] = {}
#                 try:
#                     target[date][k]
#                 except KeyError:
#                     target[date][k] = {}
#
#                 # saves 'values' tuple: (n, population, pro100k)
#                 target[date][k] = values
#         else:
#             print("skip impertinent date")
#
#     return kom_dat


def missing_data(chk: list, data: dict) -> bool:
    """ tests list in 'chk' for missing data """
    ctrl = len(chk)
    bad = ['NA', 'NA', 'NA', 'NA'] # diff_n if incorrect input
    test = [ k for k in data.keys() if data[k]['diff_n'] == bad ]
    if len(test) == ctrl:
        return True
    return False


def is_fresh_data(url:str) -> bool:
    """ Checks whether URL is live or 404 """
    ok_status = [200, 201, 202, 203, 204, 205, 206]
    try:
        test = httpx.get(url, headers={"Range": "bytes=0-100"})
        if test.status_code in ok_status:
            return True
        return False
    except:
        return False


def query_data(
                 in_dates:list,
                 big_book:dict,
                 selection: list,
                 query_object: Type[Norway]
                 ):
    """
    This is where we fetch and produce new data
    in_dates = approved datapoints (going back MAX_DATA_AGE days)
    big_book = input dictionary
    selection = muncipalities to query
    query_object =
    big_book = big_book dictionary name
    """

    # anonymous dictionary we export with return
    # that fits the selection criteria only (instead of cruft)
    small_book = {}

    # We will need:
    #   diff since yesterday
    #   diff since last 3 days
    #   diff since last week
    #   diff since last 2 weeks
    today = in_dates[0]
    yesterday = in_dates[1]

    # These must be calculated
    real_today = datetime.datetime.today()
    real_today = get_nearest_businessday(real_today)
    three_days = (real_today - BDay(3)).isoformat().split(sep="T")[0]
    a_week_ago = (real_today - BDay(5)).isoformat().split(sep="T")[0]
    two_weeks_ago = (real_today - BDay(10)).isoformat().split(sep="T")[0]

    # use a list
    pertinent_dates = [today, yesterday, three_days, a_week_ago, two_weeks_ago]

    # skipped items
    skipped_items = []

    # skip calc items
    # break loop if >= 10 skipped consecutive items
    skip_calc_counter = 0

    # If the selection encompasses ALL DATA, we save it to big dict
    # This decreases time spent analyzing data dramatically
    # A cron job will execute the equivalent of main() regularly
    doing_all = False
    if len(selection) == len(query_object.data):
        doing_all = True
        categories_count = [0, 0, 0, 0, 0] # green, orange, red, infected, N
        print(f"doing_all: {doing_all}") # debug

    for kid in selection:
        try:
            _trash = small_book[kid]
        except KeyError:
            try:
                small_book[kid] = query_object.data[kid]
            except KeyError as e:
                # TBD, we can look it up etc. TODO
                print(f"Key not in query_object: {e} (skipping)")
                skipped_items.append((kid, None))
                continue # skip

        # set kommune name to k
        k = small_book[kid]['name']
        alt = small_book[kid]['alt']

        try:
            # See if we have up-to-date info
            # today is always in pertinent dates
            _trash = small_book[kid][today]
        except KeyError:
            # get straight totals
            for date in pertinent_dates:
                # select tuple source first
                try:
                    enn, population, *pro100k = big_book['ro'][date][kid]
                    pro100k = pro100k[0] # hack
                except KeyError as e:
                    print(f"got keyerror on: {str(e)}")
                    print(f"was searching big_book['ro'][{date}][{kid}]")
                    print(f"date is {type(date)} and kid is {type(kid)}")
                    enn, population, pro100k = 'NA', 'NA', 'NA'
                    skipped_items.append((kid, date))



                try:
                    small_book[kid][date]
                except KeyError:
                    small_book[kid][date] = {}

                summary = {
                          'total_n': enn,
                          'total_pop': population,
                          'total_pro100k': pro100k
                          }

                # Save to query dict
                small_book[kid][date] = summary
                if date == today:
                    small_book[kid]['today'] = summary

                # Save to on-disk dict
                try:
                    _trash = big_book[kid]
                except KeyError:
                    big_book[kid] = {}

                big_book[kid][date] = summary

            # Differences between today and yesterday
            try:
                _fresh = small_book[kid]['updated']
                if _fresh == today: continue
            except KeyError:
                small_book[kid]['updated'] = today

            # calculate diffs
            for dtype in "total_n", "total_pro100k":
                now = big_book[kid][today][dtype]
                diff_one = big_book[kid][yesterday][dtype]
                diff_three = big_book[kid][three_days][dtype]
                diff_five = big_book[kid][a_week_ago][dtype]
                diff_ten = big_book[kid][two_weeks_ago][dtype]
                skip_calc = False

                # check before calc
                for ins in now, diff_one, diff_three, diff_five, diff_ten:
                    if type(ins) is str: skip_calc = True ; break

                # store NA or diff
                dtitle = "diff_n" if dtype == "total_n" else "diff_100k"

                # last check
                if skip_calc:
                    big_book[kid][dtitle] = ['NA', 'NA', 'NA', 'NA']
                    big_book[kid]["risk"] = 3 # N/A
                    print(f"Warning: got skip_calc for {kid}")
                    skip_calc_counter += 1
                    if skip_calc_counter >= 10:
                        break
                else:
                    skip_calc_counter = 0 # reset


                    diff_one = now - diff_one
                    diff_three = now - diff_three
                    diff_five = now - diff_five
                    diff_ten = now - diff_ten
                    #diffs = [diff_one, diff_three, diff_five, diff_ten] # all as list

                    # Order changed due to read loop
                    diffs = [diff_ten, diff_five, diff_three, diff_one]
                    big_book[kid][dtitle] = [0 if x < 0 else x for x in diffs]

                    # Update if we're doing all
                    if doing_all and diff_one > 0:
                        categories_count[3] += 1

                    # EU risk assessment (pro100k diff last 14 days)
                    if dtype == "total_pro100k":
                        pro100_was = big_book[kid][two_weeks_ago][dtype]
                        pro100_is = big_book[kid][today][dtype]
                        diff_test = pro100_is - pro100_was
                        if type(diff_test) is str:
                            big_book[kid]["risk"] = 3 # N/A
                        else:
                            if diff_test < 25:
                                risk = 0 # green
                            elif diff_test > 150:
                                risk = 2 # red
                            else:
                                risk = 1 # orange

                            # save it
                            big_book[kid]["risk"] =risk

                            if doing_all:
                                categories_count[risk] +=1

                # Save to small book too
                small_book[kid][dtitle] = big_book[kid][dtitle]

                if skip_calc_counter >= 10:
                    break

            # Set risk assessment for muncipality
            small_book[kid]["risk"] = big_book[kid]["risk"]

            if skip_calc_counter >= 10:
                break

    # Integrity check
    run_integrity_check = False
    if len(skipped_items) == len(selection):
        run_integrity_check = True
    elif skip_calc_counter >= 10:
        run_integrity_check = True

    if run_integrity_check:
        try:
            is_cloud = os.environ["heroku_is_cloud"]
            is_cloud = True if is_cloud == "1" else False
        except:
            is_cloud = False

        if is_cloud:
            pass # leave it to scheduled task
        else:
            asyncio.run(check_data_integrity())


    # national info
    # Using dummy key '0000' for the Kingdom of Norway
    try:
        small_book['0000']
    except:
        small_book['0000'] = {}

    if doing_all:
        try:
            n, po, *pro = big_book['ro'][today]['0000']
            pro = pro[0]
            try:
#                diff_n = big_book['ro']['2020-11-11']['0000'][0] # WTF
                diff_n = big_book['ro'][two_weeks_ago]['0000'][0]
                if type(diff_n) is str:
                    pass
                else:
                    diff_n = n - diff_n
                    if diff_n < 0: diff_n = 0
            except:
                diff_n = 'NA'
        except:
            n, po, pro, diff_n = 'NA', 'NA', 'NA', 'NA'

        summary = {
                    'total_n': n,
                    'total_pop': po,
                    'total_pro100k': pro,
                    'diff_n': diff_n,
                    'infected': categories_count[3],
                    'green': categories_count[0],
                    'orange': categories_count[1],
                    'red': categories_count[2]
                   }
        try:
            big_book['0000']
        except:
            big_book['0000'] ={}

        # save to disk
        big_book['0000'][today] = summary
    else:
        try:
            summary = big_book['0000'][today]
        except:
            summary = {
                        'total_n': 'NA',
                        'total_pop': 'NA',
                        'total_pro100k': 'NA',
                        'diff_n': 'NA', # number of new infected people last 24 hrs
                        'infected': 'NA', # muncipalities with infected (bool)
                        'green': 'NA', # muncipalities
                        'orange': 'NA',
                        'red': 'NA'
                       }
    # infected: muncipalities with positive diff since yesterday

    # save to end-user
    small_book['0000'] = summary


    # return dict to end-user
    return small_book, skipped_items


def get_nearest_businessday(day:datetime) -> datetime:
    """ returns nearest historical business day """
    while day.isoweekday() > 5:
        day = day + datetime.timedelta(days=-1)
    return day


def get_datapoints(
                   max_days:int,
                   query_object: Type[Folkehelseinstituttet]
                   ) -> Tuple[list, list]:
    """
    select datapoints to fetch, return a list with dates
    keep in mind there are no data points in the weekends
    """

    # Check if there's fresh data today, otherwise move back
    real_today = query_object.today
    if query_object.fresh is None:
        todays_data = query_object.msis_url(real_today)
        query_object.fresh = is_fresh_data(todays_data)
        #print(f"fresh_data available: {query_object.fresh}")

    # Set artificial today
    today = datetime.datetime.today()
    today = get_nearest_businessday(today)

    # push back 1 day if source is stale
    if not query_object.fresh:
        today = today - BDay(1)


    tstamps = []
    for i in range(max_days):
        weekday = today - BDay(i)
        tstamps.append(weekday)

    datapoints = []
    for i in tstamps:
        date_as_string = i.isoformat().split(sep="T")[0]
        datapoints.append(date_as_string)

    tstamps.sort(reverse=True)
    datapoints.sort(reverse=True)
    assert len(tstamps) == max_days
    assert len(datapoints) == max_days
    return tstamps, datapoints


def app_verify_setup():
    """ Just checks that we're up and running alright """
    try:
        s.is_setup
    except:
        s = app_korona_setup()
    return s

def norwegian_date(dato:str, short:bool) -> str:
    """ Returns short Norwegian date from YYYY-MM-DD """
    maaned = ['jan', 'feb', 'mars', 'april', 'mai', 'juni', 'juli',
              'aug', 'sep', 'okt', 'nov', 'des', 'januar', 'februar',
              'mars', 'april','mai', 'juni', 'juli', 'august',
              'september','oktober', 'november', 'desember']
    aar, mnd, dag = dato.split(sep="-")
    mnd = int(mnd)-1 if short else int(mnd)+11
    return f"{int(dag)}. {maaned[mnd]} {aar}"


def app_get_items(query_items: list) -> Tuple[list, bool]:
    """
    Used by routes:fritekst to construct list of input
    Can also be used to get fylke list, e.g.
        app_get_items(s.norge.nordland)
        app_get_items(s.norge.fylke['Nordland'])
    """
    s = app_verify_setup()
    query_items = [ x.strip() for x in query_items ]
    verified_items = []
    is_query_type = None

    # Central resources
    sammenslatt = s.norge.sammenslaatt() # conjugated names
    fylke_lists = s.norge.fylke_url_lookup # URL to item list
    postnummer = s.norge.postal_codes_2020 # lookup 2020 postal codes

    #print(f"received {query_items}")

    for item in query_items:
        # if item is four digits (e.g. 3038)
        if item.isdigit() and len(item) == 4:
            rec = s.norge.data.get(item, None)
            if rec is None: continue
            if rec == '0000': continue
            verified_items.append(item)
            is_query_type = 0
            continue

        # check postal codes (prefixed with N, eg. "N0001")
        if len(item) == 5 and item[:1].upper() == "N":
            rec = postnummer.get(item.lower(), None)
            if rec is None:
                pass
            else:
                verified_items.append(rec)
                is_query_type = 0

        # capitalize Query
        if item.lower() in sammenslatt:
            a, b = item.split(sep=" og ") # saami "ja" goes in alt-check below
            q = f"{a.capitalize()} og {b.capitalize()}"
        else:
            q = item.capitalize()

        # if alternate spelling use standard
        alt = [ k for k,v in s.norge.alt_name.items() if q.lower() in v.lower() ]
        if len(alt) == 1: q = alt[0]

        # check if fylke
        if q in s.norge.fylker.keys():
            _ = [
                 verified_items.append(s.norge.lookup(k))
                 for k in s.norge.fylker[q]
                 if s.norge.lookup(k) not in verified_items
                 ]

            if len(query_items) == 1:
                if is_query_type is None: is_query_type = 1
                continue
        elif q.lower() in fylke_lists.keys():
            _ = [ verified_items.append(s.norge.lookup(k))
                for k in fylke_lists.get(q.lower())
                if s.norge.lookup(k) not in verified_items
                ]

            if len(query_items) == 1:
                if is_query_type is None: is_query_type = 1
                continue

        # or special case / custom query
        if item in s.custom_queries.keys():
            _ = [
                verified_items.append(s.norge.lookup(k))
                for k in s.custom_queries[item]['list']
                if s.norge.lookup(k) not in verified_items
                ]
            is_query_type = 2
            break

        is_query_type = 0
        # or lookup string in lookup func
        verified_items.append(s.norge.lookup(item))

    #print("debug query")
    #print(f"query_items {query_items}")
    #print(f"verified_items: {verified_items}")

    # Remove any empty strings from norge.lookup()
    return (list(filter(None, verified_items)), is_query_type)


def app_query(query_items: list) -> dict:
    """
    Used by app:app to query files
    Assumes data has been vetted by app_get_items() or manually
    with some hardcoded selection, e.g. s.norge.innlandet
    """
    s = app_verify_setup()

    get_dates = s.datapoints
    source = s.book
    lookup = s.norge

    # Query sources and return dictionary to app
    data, skipped_items = query_data(get_dates, source, query_items, lookup)
    return data, skipped_items


def app_get_plotdata(item_id: str, data_type: int) -> dict:
    """
    Returns data dict for item ID to be used in panda/seaborn
    data_types in 0-2 from tuple: (n, po, pro, k)
    """
    s = app_verify_setup()

    # Will always return valid dict for seaborn
    if data_type in [0,1,2]:
        pass
    else:
        data_type = 0

    if item_id in s.norge.data.keys():
        pass
    else:
        item_id = '0000'

    # Get data
    x_axis = [ x for x in s.datapoints ] # values not references
    x_axis.reverse() # order
    y_axis = [ s.book['ro'][y][item_id][data_type] for y in x_axis ]

    # set labels
    if data_type == 0:
        x_label, y_label = "dato", "total_n"
    elif data_type == 1:
        x_label, y_label = "dato", "total_pop"
    elif data_type == 2:
        x_label, y_label = "dato", "per_100k"

    # Return dict for pd.DataFrame / Seaborn
    # dat = pd.DataFrame(korona.app_get_plotdata(5401,0))
    return {f"{x_label}":x_axis, f"{y_label}":y_axis}

    # Year = [2012, 2014, 2016, 2020, 2021, 2022, 2018]
    # Profit = [80, 75.8, 74, 65, 99.5, 19, 33.6]
    # data_plot = pd.DataFrame({"Year":Year, "Profit":Profit})


def app_korona_setup():
    """ Setup minimum config to use the program or app """
    s = Session()

    # TODO
    # s.today (for real today)

    # Paths and methods related to stat source
    s.FHI = Folkehelseinstituttet(s.store)

    # Data object containing a dict of Norway
    s.norge = Norway()

    # The datapoints we're interested in
    s.tstamps, s.datapoints = get_datapoints(s.age, s.FHI)

    # Read from disk
    s.book = read_data(s.datapoints, s.store)

    # Do a tiny query (1 muncipality)
    tromso = ['5401']
    s.current, _trash = query_data(s.datapoints, s.book, tromso, s.norge)

    return s


async def missing_data(control: list, data: dict) -> bool:
    """ tests list in 'chk' for missing data """
    bad = ['NA', 'NA', 'NA', 'NA'] # diff_n if incorrect input
    test = [ k for k in data.keys() if data[k]['diff_n'] == bad ]
    if len(test) == len(control):
        return True
    return False


async def check_data_integrity():
    """ Same as setup, but will delete big_book if corrupted """
    # datetime.datetime.now().isoformat()
    #print('Data integrity check (n=10)')
    #pls_check = ['4214','4215','1144','3812','5414',
    #             '3813','1135','5439','5440','3007']
    # running app_query also runs verify setup()
    #data, _ = app_query(pls_check)
    #_kingdom = data.pop('0000')

    # file check
    #if Path(s.store).is_file():
    #    print(f'Data file: {s.store}')
    #else:
    #    print(f'Data file: {s.store} (missing)')

    # dict check
    #corrupted = await missing_data(pls_check, data)
    #if corrupted:
    #    print('Result: data corrupted')
    #else:
    #    print('Result: data OK')

    # web page check (stale cache or something)
    corrupted = False
    print("Testing debug_info data using httpx.get")
    debug_page = "https://sjekk.kommune.nu/debug_info"
    async with httpx.AsyncClient() as client:
        site = await client.get(debug_page)

    if site.is_error:
        pass # Not sure we should pass or set to reboot
    else:
        if site.text.count("NA") > 8:
            corrupted = True

    if corrupted:
        print("Cache is stale/dead, force app restart")
        right_now = datetime.datetime.now().isoformat()
        os.environ["heroku_app_restart"] = right_now
        # Changing conf var should trigger heroku restart



def main():
    """ Original main() used to setup stuff """
    print("run setup() from __main__ (localhost)")
    asyncio.run(setup(is_local=True))


async def main_cloud():
    """ heroku main() used to setup stuff """
    print("run setup() from __main__ (cloud)")
    await setup(is_local=False)
    await check_data_integrity()



async def setup(**kwargs):
    """
    Entry point or FULL setup (not minimal)
    From app, only use this in startup, otherwise use
    app_korona_setup() inside starlette.
    This exemplifies how this could be run conventionally
    """

    is_single_threaded = kwargs.get('is_local', False)

    print('init')
    elapsed = datetime.datetime.now().timestamp()

    # Initialize empty settings
    s = Session()

    # Setup FHI object that contains
    # -> link to on-disk store: FHI.store
    # -> on-disk store as dict: FHI.book
    # -> current data dict as:  FHI.current
    s.FHI = Folkehelseinstituttet(s.store)

    # Test ENV heroku config vars
    print(f"set store to {s.FHI.store}")

    # Setup staten
    s.norge = Norway()

    # for brevity
    norge = s.norge
    max_age = s.age
    FHI = s.FHI
    store = s.FHI.store
    book = s.FHI.book

    # Specify desired timeseries in a list-of-dates
    print('set datapoints') # debug
    tstamps, datapoints = get_datapoints(max_age, FHI)

    # Clean up old data entries
    FHI.resize_db = clear_data(datapoints, max_age, FHI)

    # read data from local storage to dict
    print('read data') # debug
    book = read_data(datapoints, store)

    #print(FHI.book)
    #breakpoint()

    # refresh dict and local storage
    # will fetch new data from FHI repository


    # Run refresh asynchronous
    print('refresh data') # debug
    await refresh_data(datapoints, book, store, FHI)

#    if is_single_threaded:
#        # is-single-threaded
#        asyncio.run(refresh_data(datapoints, book, store, FHI))
#    else:
#        # but on heroku we use >1 worker and get Runtime error
#        # so we can just run it async synchronously
#        await refresh_data(datapoints, book, store, FHI)


    all = list(norge.data.keys())
    print('fetch ALL') # debug
    s.FHI.current, _trash = query_data(datapoints, book, all, norge)

    #print("showing 'current' dataset NOT big book:")
    #print(FHI.current)
    #print("end-of 'current' dataset NOT big book:)")

    # Save data to disk (saves time)
    save_to_file(book, store)

    #print("showing 'current' dataset NOT big book:")
    #print(FHI.current)

    # debug timer
    elapsed = datetime.datetime.now().timestamp() - elapsed

    print(f"finished in {elapsed} seconds")

if __name__ == "__main__":
    try:
        is_cloud = os.environ["heroku_is_cloud"]
        is_cloud = True if is_cloud == "1" else False
    except:
        is_cloud = False

    if is_cloud:
        asyncio.run(main_cloud())
    else:
        main()
