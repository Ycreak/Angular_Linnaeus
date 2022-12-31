// Library imports
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { MatDialog } from '@angular/material/dialog'; // Library used for interacting with the page
import { trigger, transition, style, animate, state } from '@angular/animations';
import { filter, fromEvent, Observable, Subscription } from "rxjs";
import { ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
// Component imports
// import { LoginComponent } from '../login/login.component'

import {CollectionViewer, SelectionChange, DataSource} from '@angular/cdk/collections';
import {FlatTreeControl} from '@angular/cdk/tree';
import {Injectable} from '@angular/core';
import {BehaviorSubject, merge} from 'rxjs';
import {map} from 'rxjs/operators';

import {MatTreeNestedDataSource} from '@angular/material/tree';
import {NestedTreeControl} from '@angular/cdk/tree';

// Service imports
import { ApiService } from '../api.service';
// import { DialogService } from '../services/dialog.service';
import { UtilityService } from '../utility.service';
// import { AuthService } from '../auth/auth.service';


// Model imports
import { Fragment } from '../models/Fragment';
import { Column } from '../models/Column';
import { Sandbox } from '../models/Sandbox';

import { Introductions } from '../models/Introductions';

import my_database from './myfile6.json';

interface taxon_node {
  name: string;
  taxon: string;
  _id: string;
  children?: taxon_node[];
}

const TREE_DATA = [
  {
    "name": "Animalia",
    "taxon": "kingdom",
    "_id": "125427",
    "children": [
      {
        "name": "Arthropoda",
        "taxon": "phylum",
        "_id": "125428",
        "children": [
          {
            "name": "Crustacea",
            "taxon": "subphylum",
            "_id": "125429",
            "children": [
              {
                "name": "Maxillopoda",
                "taxon": "class",
                "_id": "125430",
                "children": [
                  {
                    "name": "Copepoda",
                    "taxon": "subclass",
                    "_id": "125431",
                    "children": [
                      {
                        "name": "Neocopepoda",
                        "taxon": "infraclass",
                        "_id": "125432",
                        "children": [
                          {
                            "name": "Gymnoplea",
                            "taxon": "superorder",
                            "_id": "125433",
                            "children": [
                              {
                                "name": "Calanoida",
                                "taxon": "order",
                                "_id": "125434",
                                "children": [
                                  {
                                    "name": "Aetideidae",
                                    "taxon": "family",
                                    "_id": "125435",
                                    "children": [
                                      {
                                        "name": "Aetideopsis",
                                        "taxon": "genus",
                                        "_id": "125436",
                                        "children": [
                                          {
                                            "name": "Aetideopsis albatrossae",
                                            "taxon": "species",
                                            "_id": "125461"
                                          },
                                          {
                                            "name": "Aetideopsis armata",
                                            "taxon": "species",
                                            "_id": "125462"
                                          },
                                          {
                                            "name": "Aetideopsis carinata",
                                            "taxon": "species",
                                            "_id": "125463"
                                          },
                                          {
                                            "name": "Aetideopsis cristata",
                                            "taxon": "species",
                                            "_id": "125464"
                                          },
                                          {
                                            "name": "Aetideopsis minor",
                                            "taxon": "species",
                                            "_id": "125465"
                                          },
                                          {
                                            "name": "Aetideopsis multiserrata",
                                            "taxon": "species",
                                            "_id": "125466"
                                          },
                                          {
                                            "name": "Aetideopsis retusa",
                                            "taxon": "species",
                                            "_id": "125467"
                                          },
                                          {
                                            "name": "Aetideopsis rostrata",
                                            "taxon": "species",
                                            "_id": "125468"
                                          },
                                          {
                                            "name": "Aetideopsis tumorosa",
                                            "taxon": "species",
                                            "_id": "125469"
                                          },
                                          {
                                            "name": "Aetideopsis albatrossae",
                                            "taxon": "species",
                                            "_id": "125461"
                                          },
                                          {
                                            "name": "Aetideopsis armata",
                                            "taxon": "species",
                                            "_id": "125462"
                                          },
                                          {
                                            "name": "Aetideopsis carinata",
                                            "taxon": "species",
                                            "_id": "125463"
                                          },
                                          {
                                            "name": "Aetideopsis cristata",
                                            "taxon": "species",
                                            "_id": "125464"
                                          },
                                          {
                                            "name": "Aetideopsis minor",
                                            "taxon": "species",
                                            "_id": "125465"
                                          },
                                          {
                                            "name": "Aetideopsis multiserrata",
                                            "taxon": "species",
                                            "_id": "125466"
                                          },
                                          {
                                            "name": "Aetideopsis retusa",
                                            "taxon": "species",
                                            "_id": "125467"
                                          },
                                          {
                                            "name": "Aetideopsis rostrata",
                                            "taxon": "species",
                                            "_id": "125468"
                                          },
                                          {
                                            "name": "Aetideopsis tumorosa",
                                            "taxon": "species",
                                            "_id": "125469"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Aetideus",
                                        "taxon": "genus",
                                        "_id": "125437",
                                        "children": [
                                          {
                                            "name": "Aetideus acutus",
                                            "taxon": "species",
                                            "_id": "125470"
                                          },
                                          {
                                            "name": "Aetideus arcuatus",
                                            "taxon": "species",
                                            "_id": "125471"
                                          },
                                          {
                                            "name": "Aetideus armatus",
                                            "taxon": "species",
                                            "_id": "125472"
                                          },
                                          {
                                            "name": "Aetideus bradyi",
                                            "taxon": "species",
                                            "_id": "125473"
                                          },
                                          {
                                            "name": "Aetideus divergens",
                                            "taxon": "species",
                                            "_id": "125474"
                                          },
                                          {
                                            "name": "Aetideus giesbrechti",
                                            "taxon": "species",
                                            "_id": "125475"
                                          },
                                          {
                                            "name": "Aetideus mexicanus",
                                            "taxon": "species",
                                            "_id": "125476"
                                          },
                                          {
                                            "name": "Aetideus pacificus",
                                            "taxon": "species",
                                            "_id": "125477"
                                          },
                                          {
                                            "name": "Aetideus pseudarmatus",
                                            "taxon": "species",
                                            "_id": "125478"
                                          },
                                          {
                                            "name": "Aetideus truncatus",
                                            "taxon": "species",
                                            "_id": "125479"
                                          },
                                          {
                                            "name": "Aetideus acutus",
                                            "taxon": "species",
                                            "_id": "125470"
                                          },
                                          {
                                            "name": "Aetideus arcuatus",
                                            "taxon": "species",
                                            "_id": "125471"
                                          },
                                          {
                                            "name": "Aetideus armatus",
                                            "taxon": "species",
                                            "_id": "125472"
                                          },
                                          {
                                            "name": "Aetideus bradyi",
                                            "taxon": "species",
                                            "_id": "125473"
                                          },
                                          {
                                            "name": "Aetideus divergens",
                                            "taxon": "species",
                                            "_id": "125474"
                                          },
                                          {
                                            "name": "Aetideus giesbrechti",
                                            "taxon": "species",
                                            "_id": "125475"
                                          },
                                          {
                                            "name": "Aetideus mexicanus",
                                            "taxon": "species",
                                            "_id": "125476"
                                          },
                                          {
                                            "name": "Aetideus pacificus",
                                            "taxon": "species",
                                            "_id": "125477"
                                          },
                                          {
                                            "name": "Aetideus pseudarmatus",
                                            "taxon": "species",
                                            "_id": "125478"
                                          },
                                          {
                                            "name": "Aetideus truncatus",
                                            "taxon": "species",
                                            "_id": "125479"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Azygokeras",
                                        "taxon": "genus",
                                        "_id": "125438",
                                        "children": [
                                          {
                                            "name": "Azygokeras columbiae",
                                            "taxon": "species",
                                            "_id": "125480"
                                          },
                                          {
                                            "name": "Azygokeras columbiae",
                                            "taxon": "species",
                                            "_id": "125480"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Batheuchaeta",
                                        "taxon": "genus",
                                        "_id": "125439",
                                        "children": [
                                          {
                                            "name": "Batheuchaeta anomala",
                                            "taxon": "species",
                                            "_id": "125481"
                                          },
                                          {
                                            "name": "Batheuchaeta antarctica",
                                            "taxon": "species",
                                            "_id": "125482"
                                          },
                                          {
                                            "name": "Batheuchaeta gurjanovae",
                                            "taxon": "species",
                                            "_id": "125483"
                                          },
                                          {
                                            "name": "Batheuchaeta heptneri",
                                            "taxon": "species",
                                            "_id": "125484"
                                          },
                                          {
                                            "name": "Batheuchaeta lamellata",
                                            "taxon": "species",
                                            "_id": "125485"
                                          },
                                          {
                                            "name": "Batheuchaeta peculiaris",
                                            "taxon": "species",
                                            "_id": "125486"
                                          },
                                          {
                                            "name": "Batheuchaeta pubescens",
                                            "taxon": "species",
                                            "_id": "125487"
                                          },
                                          {
                                            "name": "Batheuchaeta tuberculata",
                                            "taxon": "species",
                                            "_id": "125488"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Bradyetes",
                                        "taxon": "genus",
                                        "_id": "125440",
                                        "children": [
                                          {
                                            "name": "Bradyetes inermis",
                                            "taxon": "species",
                                            "_id": "125489"
                                          },
                                          {
                                            "name": "Bradyetes matthei",
                                            "taxon": "species",
                                            "_id": "125490"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Bradyidius",
                                        "taxon": "genus",
                                        "_id": "125441",
                                        "children": [
                                          {
                                            "name": "Bradyidius angustus",
                                            "taxon": "species",
                                            "_id": "125491"
                                          },
                                          {
                                            "name": "Bradyidius armatus",
                                            "taxon": "species",
                                            "_id": "125492"
                                          },
                                          {
                                            "name": "Bradyidius arnoldi",
                                            "taxon": "species",
                                            "_id": "125493"
                                          },
                                          {
                                            "name": "Bradyidius curtus",
                                            "taxon": "species",
                                            "_id": "125494"
                                          },
                                          {
                                            "name": "Bradyidius luluae",
                                            "taxon": "species",
                                            "_id": "125495"
                                          },
                                          {
                                            "name": "Bradyidius pacificus",
                                            "taxon": "species",
                                            "_id": "125496"
                                          },
                                          {
                                            "name": "Bradyidius rakuma",
                                            "taxon": "species",
                                            "_id": "125497"
                                          },
                                          {
                                            "name": "Bradyidius saanichi",
                                            "taxon": "species",
                                            "_id": "125498"
                                          },
                                          {
                                            "name": "Bradyidius similis",
                                            "taxon": "species",
                                            "_id": "125499"
                                          },
                                          {
                                            "name": "Bradyidius subarmatus",
                                            "taxon": "species",
                                            "_id": "125500"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Chiridiella",
                                        "taxon": "genus",
                                        "_id": "125442",
                                        "children": [
                                          {
                                            "name": "Chiridiella abyssalis",
                                            "taxon": "species",
                                            "_id": "125501"
                                          },
                                          {
                                            "name": "Chiridiella bichela",
                                            "taxon": "species",
                                            "_id": "125502"
                                          },
                                          {
                                            "name": "Chiridiella bispinosa",
                                            "taxon": "species",
                                            "_id": "125503"
                                          },
                                          {
                                            "name": "Chiridiella brachydactyla",
                                            "taxon": "species",
                                            "_id": "125504"
                                          },
                                          {
                                            "name": "Chiridiella brooksi",
                                            "taxon": "species",
                                            "_id": "125505"
                                          },
                                          {
                                            "name": "Chiridiella chainae",
                                            "taxon": "species",
                                            "_id": "125506"
                                          },
                                          {
                                            "name": "Chiridiella gibba",
                                            "taxon": "species",
                                            "_id": "125507"
                                          },
                                          {
                                            "name": "Chiridiella kuniae",
                                            "taxon": "species",
                                            "_id": "125508"
                                          },
                                          {
                                            "name": "Chiridiella macrodactyla",
                                            "taxon": "species",
                                            "_id": "125509"
                                          },
                                          {
                                            "name": "Chiridiella ovata",
                                            "taxon": "species",
                                            "_id": "125510"
                                          },
                                          {
                                            "name": "Chiridiella pacifica",
                                            "taxon": "species",
                                            "_id": "125511"
                                          },
                                          {
                                            "name": "Chiridiella reductella",
                                            "taxon": "species",
                                            "_id": "125512"
                                          },
                                          {
                                            "name": "Chiridiella sarsi",
                                            "taxon": "species",
                                            "_id": "125513"
                                          },
                                          {
                                            "name": "Chiridiella smoki",
                                            "taxon": "species",
                                            "_id": "125514"
                                          },
                                          {
                                            "name": "Chiridiella subaequalis",
                                            "taxon": "species",
                                            "_id": "125515"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Chiridius",
                                        "taxon": "genus",
                                        "_id": "125443",
                                        "children": [
                                          {
                                            "name": "Chiridius gracilis",
                                            "taxon": "species",
                                            "_id": "125516"
                                          },
                                          {
                                            "name": "Chiridius longispinus",
                                            "taxon": "species",
                                            "_id": "125517"
                                          },
                                          {
                                            "name": "Chiridius molestus",
                                            "taxon": "species",
                                            "_id": "125518"
                                          },
                                          {
                                            "name": "Chiridius obtusifrons",
                                            "taxon": "species",
                                            "_id": "125519"
                                          },
                                          {
                                            "name": "Chiridius pacificus",
                                            "taxon": "species",
                                            "_id": "125520"
                                          },
                                          {
                                            "name": "Chiridius polaris",
                                            "taxon": "species",
                                            "_id": "125521"
                                          },
                                          {
                                            "name": "Chiridius poppei",
                                            "taxon": "species",
                                            "_id": "125522"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Chirundina",
                                        "taxon": "genus",
                                        "_id": "125444",
                                        "children": [
                                          {
                                            "name": "Chirundina alaskaensis",
                                            "taxon": "species",
                                            "_id": "125523"
                                          },
                                          {
                                            "name": "Chirundina indica",
                                            "taxon": "species",
                                            "_id": "125524"
                                          },
                                          {
                                            "name": "Chirundina streetsii",
                                            "taxon": "species",
                                            "_id": "125525"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Chirundinella",
                                        "taxon": "genus",
                                        "_id": "125445",
                                        "children": [
                                          {
                                            "name": "Chirundinella magna",
                                            "taxon": "species",
                                            "_id": "125526"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Comantenna",
                                        "taxon": "genus",
                                        "_id": "125446",
                                        "children": [
                                          {
                                            "name": "Comantenna brevicornis",
                                            "taxon": "species",
                                            "_id": "125527"
                                          },
                                          {
                                            "name": "Comantenna crassa",
                                            "taxon": "species",
                                            "_id": "125528"
                                          },
                                          {
                                            "name": "Comantenna curtisetosa",
                                            "taxon": "species",
                                            "_id": "125529"
                                          },
                                          {
                                            "name": "Comantenna recurvata",
                                            "taxon": "species",
                                            "_id": "125530"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Crassantenna",
                                        "taxon": "genus",
                                        "_id": "125447",
                                        "children": [
                                          {
                                            "name": "Crassantenna comosa",
                                            "taxon": "species",
                                            "_id": "125531"
                                          },
                                          {
                                            "name": "Crassantenna mimorostrata",
                                            "taxon": "species",
                                            "_id": "125532"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Euchirella",
                                        "taxon": "genus",
                                        "_id": "125448",
                                        "children": [
                                          {
                                            "name": "Euchirella amoena",
                                            "taxon": "species",
                                            "_id": "125533"
                                          },
                                          {
                                            "name": "Euchirella bella",
                                            "taxon": "species",
                                            "_id": "125534"
                                          },
                                          {
                                            "name": "Euchirella bitumida",
                                            "taxon": "species",
                                            "_id": "125535"
                                          },
                                          {
                                            "name": "Euchirella curticauda",
                                            "taxon": "species",
                                            "_id": "125536"
                                          },
                                          {
                                            "name": "Euchirella formosa",
                                            "taxon": "species",
                                            "_id": "125537"
                                          },
                                          {
                                            "name": "Euchirella galeata",
                                            "taxon": "species",
                                            "_id": "125538"
                                          },
                                          {
                                            "name": "Euchirella grandicornis",
                                            "taxon": "species",
                                            "_id": "125539"
                                          },
                                          {
                                            "name": "Euchirella maxima",
                                            "taxon": "species",
                                            "_id": "125540"
                                          },
                                          {
                                            "name": "Euchirella messinensis",
                                            "taxon": "species",
                                            "_id": "125541"
                                          },
                                          {
                                            "name": "Euchirella pseudopulchra",
                                            "taxon": "species",
                                            "_id": "125542"
                                          },
                                          {
                                            "name": "Euchirella pseudotruncata",
                                            "taxon": "species",
                                            "_id": "125543"
                                          },
                                          {
                                            "name": "Euchirella pulchra",
                                            "taxon": "species",
                                            "_id": "125544"
                                          },
                                          {
                                            "name": "Euchirella rostrata",
                                            "taxon": "species",
                                            "_id": "125545"
                                          },
                                          {
                                            "name": "Euchirella similis",
                                            "taxon": "species",
                                            "_id": "125546"
                                          },
                                          {
                                            "name": "Euchirella speciosa",
                                            "taxon": "species",
                                            "_id": "125547"
                                          },
                                          {
                                            "name": "Euchirella splendens",
                                            "taxon": "species",
                                            "_id": "125548"
                                          },
                                          {
                                            "name": "Euchirella truncata",
                                            "taxon": "species",
                                            "_id": "125549"
                                          },
                                          {
                                            "name": "Euchirella unispina",
                                            "taxon": "species",
                                            "_id": "125550"
                                          },
                                          {
                                            "name": "Euchirella venusta",
                                            "taxon": "species",
                                            "_id": "125551"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Gaetanus",
                                        "taxon": "genus",
                                        "_id": "125449",
                                        "children": [
                                          {
                                            "name": "Gaetanus antarcticus",
                                            "taxon": "species",
                                            "_id": "125552"
                                          },
                                          {
                                            "name": "Gaetanus armiger",
                                            "taxon": "species",
                                            "_id": "125553"
                                          },
                                          {
                                            "name": "Gaetanus brachyurus",
                                            "taxon": "species",
                                            "_id": "125554"
                                          },
                                          {
                                            "name": "Gaetanus brevicaudatus",
                                            "taxon": "species",
                                            "_id": "125555"
                                          },
                                          {
                                            "name": "Gaetanus brevicornis",
                                            "taxon": "species",
                                            "_id": "125556"
                                          },
                                          {
                                            "name": "Gaetanus brevirostris",
                                            "taxon": "species",
                                            "_id": "125557"
                                          },
                                          {
                                            "name": "Gaetanus brevispinus",
                                            "taxon": "species",
                                            "_id": "125558"
                                          },
                                          {
                                            "name": "Gaetanus curvicornis",
                                            "taxon": "species",
                                            "_id": "125559"
                                          },
                                          {
                                            "name": "Gaetanus inermis",
                                            "taxon": "species",
                                            "_id": "125560"
                                          },
                                          {
                                            "name": "Gaetanus kruppii",
                                            "taxon": "species",
                                            "_id": "125561"
                                          },
                                          {
                                            "name": "Gaetanus latifrons",
                                            "taxon": "species",
                                            "_id": "125562"
                                          },
                                          {
                                            "name": "Gaetanus miles",
                                            "taxon": "species",
                                            "_id": "125563"
                                          },
                                          {
                                            "name": "Gaetanus minispinus",
                                            "taxon": "species",
                                            "_id": "125564"
                                          },
                                          {
                                            "name": "Gaetanus minor",
                                            "taxon": "species",
                                            "_id": "125565"
                                          },
                                          {
                                            "name": "Gaetanus minutus",
                                            "taxon": "species",
                                            "_id": "125566"
                                          },
                                          {
                                            "name": "Gaetanus paracurvicornis",
                                            "taxon": "species",
                                            "_id": "125567"
                                          },
                                          {
                                            "name": "Gaetanus pileatus",
                                            "taxon": "species",
                                            "_id": "125568"
                                          },
                                          {
                                            "name": "Gaetanus pseudolatifrons",
                                            "taxon": "species",
                                            "_id": "125569"
                                          },
                                          {
                                            "name": "Gaetanus pungens",
                                            "taxon": "species",
                                            "_id": "125570"
                                          },
                                          {
                                            "name": "Gaetanus robustus",
                                            "taxon": "species",
                                            "_id": "125571"
                                          },
                                          {
                                            "name": "Gaetanus rubellus",
                                            "taxon": "species",
                                            "_id": "125572"
                                          },
                                          {
                                            "name": "Gaetanus secundus",
                                            "taxon": "species",
                                            "_id": "125573"
                                          },
                                          {
                                            "name": "Gaetanus simplex",
                                            "taxon": "species",
                                            "_id": "125574"
                                          },
                                          {
                                            "name": "Gaetanus tenuispinus",
                                            "taxon": "species",
                                            "_id": "125575"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Jaschnovia",
                                        "taxon": "genus",
                                        "_id": "125450",
                                        "children": [
                                          {
                                            "name": "Jaschnovia brevis",
                                            "taxon": "species",
                                            "_id": "125576"
                                          },
                                          {
                                            "name": "Jaschnovia tolli",
                                            "taxon": "species",
                                            "_id": "125577"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Lutamator",
                                        "taxon": "genus",
                                        "_id": "125451",
                                        "children": [
                                          {
                                            "name": "Lutamator elegans",
                                            "taxon": "species",
                                            "_id": "125578"
                                          },
                                          {
                                            "name": "Lutamator hurlei",
                                            "taxon": "species",
                                            "_id": "125579"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Mesocomantenna",
                                        "taxon": "genus",
                                        "_id": "125452",
                                        "children": [
                                          {
                                            "name": "Mesocomantenna spinosa",
                                            "taxon": "species",
                                            "_id": "125580"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Paivella",
                                        "taxon": "genus",
                                        "_id": "125453",
                                        "children": [
                                          {
                                            "name": "Paivella inaciae",
                                            "taxon": "species",
                                            "_id": "125581"
                                          },
                                          {
                                            "name": "Paivella naporai",
                                            "taxon": "species",
                                            "_id": "125582"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Paracomantenna",
                                        "taxon": "genus",
                                        "_id": "125454",
                                        "children": [
                                          {
                                            "name": "Paracomantenna gracilis",
                                            "taxon": "species",
                                            "_id": "125583"
                                          },
                                          {
                                            "name": "Paracomantenna magalyae",
                                            "taxon": "species",
                                            "_id": "125584"
                                          },
                                          {
                                            "name": "Paracomantenna minor",
                                            "taxon": "species",
                                            "_id": "125585"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Pseudeuchaeta",
                                        "taxon": "genus",
                                        "_id": "125455",
                                        "children": [
                                          {
                                            "name": "Pseudeuchaeta arctica",
                                            "taxon": "species",
                                            "_id": "125586"
                                          },
                                          {
                                            "name": "Pseudeuchaeta brevicauda",
                                            "taxon": "species",
                                            "_id": "125587"
                                          },
                                          {
                                            "name": "Pseudeuchaeta flexuosa",
                                            "taxon": "species",
                                            "_id": "125588"
                                          },
                                          {
                                            "name": "Pseudeuchaeta magna",
                                            "taxon": "species",
                                            "_id": "125589"
                                          },
                                          {
                                            "name": "Pseudeuchaeta major",
                                            "taxon": "species",
                                            "_id": "125590"
                                          },
                                          {
                                            "name": "Pseudeuchaeta spinata",
                                            "taxon": "species",
                                            "_id": "125591"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Pseudochirella",
                                        "taxon": "genus",
                                        "_id": "125456",
                                        "children": [
                                          {
                                            "name": "Pseudochirella accepta",
                                            "taxon": "species",
                                            "_id": "125592"
                                          },
                                          {
                                            "name": "Pseudochirella batillipa",
                                            "taxon": "species",
                                            "_id": "125593"
                                          },
                                          {
                                            "name": "Pseudochirella bilobata",
                                            "taxon": "species",
                                            "_id": "125594"
                                          },
                                          {
                                            "name": "Pseudochirella bowmani",
                                            "taxon": "species",
                                            "_id": "125595"
                                          },
                                          {
                                            "name": "Pseudochirella dentata",
                                            "taxon": "species",
                                            "_id": "125596"
                                          },
                                          {
                                            "name": "Pseudochirella divaricata",
                                            "taxon": "species",
                                            "_id": "125597"
                                          },
                                          {
                                            "name": "Pseudochirella dubia",
                                            "taxon": "species",
                                            "_id": "125598"
                                          },
                                          {
                                            "name": "Pseudochirella fallax",
                                            "taxon": "species",
                                            "_id": "125599"
                                          },
                                          {
                                            "name": "Pseudochirella formosa",
                                            "taxon": "species",
                                            "_id": "125600"
                                          },
                                          {
                                            "name": "Pseudochirella gibbera",
                                            "taxon": "species",
                                            "_id": "125601"
                                          },
                                          {
                                            "name": "Pseudochirella hirsuta",
                                            "taxon": "species",
                                            "_id": "125602"
                                          },
                                          {
                                            "name": "Pseudochirella limata",
                                            "taxon": "species",
                                            "_id": "125603"
                                          },
                                          {
                                            "name": "Pseudochirella lobata",
                                            "taxon": "species",
                                            "_id": "125604"
                                          },
                                          {
                                            "name": "Pseudochirella mariana",
                                            "taxon": "species",
                                            "_id": "125605"
                                          },
                                          {
                                            "name": "Pseudochirella mawsoni",
                                            "taxon": "species",
                                            "_id": "125606"
                                          },
                                          {
                                            "name": "Pseudochirella notacantha",
                                            "taxon": "species",
                                            "_id": "125607"
                                          },
                                          {
                                            "name": "Pseudochirella obesa",
                                            "taxon": "species",
                                            "_id": "125608"
                                          },
                                          {
                                            "name": "Pseudochirella obtusa",
                                            "taxon": "species",
                                            "_id": "125609"
                                          },
                                          {
                                            "name": "Pseudochirella pacifica",
                                            "taxon": "species",
                                            "_id": "125610"
                                          },
                                          {
                                            "name": "Pseudochirella palliata",
                                            "taxon": "species",
                                            "_id": "125611"
                                          },
                                          {
                                            "name": "Pseudochirella pustulifera",
                                            "taxon": "species",
                                            "_id": "125612"
                                          },
                                          {
                                            "name": "Pseudochirella scopularis",
                                            "taxon": "species",
                                            "_id": "125613"
                                          },
                                          {
                                            "name": "Pseudochirella spectabilis",
                                            "taxon": "species",
                                            "_id": "125614"
                                          },
                                          {
                                            "name": "Pseudochirella spinosa",
                                            "taxon": "species",
                                            "_id": "125615"
                                          },
                                          {
                                            "name": "Pseudochirella tanakai",
                                            "taxon": "species",
                                            "_id": "125616"
                                          },
                                          {
                                            "name": "Pseudochirella vervoorti",
                                            "taxon": "species",
                                            "_id": "125617"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Pterochirella",
                                        "taxon": "genus",
                                        "_id": "125457",
                                        "children": [
                                          {
                                            "name": "Pterochirella tuerkayi",
                                            "taxon": "species",
                                            "_id": "125618"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Senecella",
                                        "taxon": "genus",
                                        "_id": "125458",
                                        "children": [
                                          {
                                            "name": "Senecella calanoides",
                                            "taxon": "species",
                                            "_id": "125619"
                                          },
                                          {
                                            "name": "Senecella siberica",
                                            "taxon": "species",
                                            "_id": "125620"
                                          }
                                        ]
                                      },
                                      {
                                        "name": "Sursamucro",
                                        "taxon": "genus",
                                        "_id": "125459",
                                        "children": [
                                          {
                                            "name": "Sursamucro spinatus",
                                            "taxon": "species",
                                            "_id": "125621"
                                          }
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
]

@Component({
  selector: 'app-fragments',
  templateUrl: './fragments.component.html',
  styleUrls: ['./fragments.component.scss'],
  encapsulation: ViewEncapsulation.None,
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
    trigger('fadeSlideInOut', [
      transition(':enter', [
          style({ opacity: 0, transform: 'translateY(10px)' }),
          animate('500ms', style({ opacity: 1, transform: 'translateY(0)' })),
      ]),
      transition(':leave', [
          animate('500ms', style({ opacity: 0, transform: 'translateY(10px)' })),
      ]),
    ]),
  ],
})

export class FragmentsComponent implements OnInit {
  
  window_resize_observable$: Observable<Event>
  window_resize_subscription$: Subscription

  //TODO: this should be system wide
  oscc_settings = { 
    dragging_disabled : false, 
    fragment_order_gradient : false,
    auto_scroll_linked_fragments : false,
    show_headers : true, 
    show_line_names : true, 
  }; 

  // Toggle switches for the HTML columns/modes
  commentary_enabled: boolean = true;
  playground_enabled: boolean = false;
  // Booleans for HTML related items
  spinner: boolean = false; // Boolean to toggle the spinner.
  server_down: boolean = true; // to indicate server failure
  // Global Class Variables with text data corresponding to the front-end text fields.
  current_fragment: Fragment; // Variable to store the clicked fragment and its data
  fragment_clicked: boolean = false; // Shows "click a fragment" banner at startup if nothing is yet selected

  // Object to store all column data: just an array with column data in the form of fragment columns
  columns: Column[] = [];

  // Data columns
  column1: Column;
  column2: Column;
  column3: Column;
  column4: Column;
  playground: Column;
  commentary_column: Column;

  // We keep track of the number of columns to identify them
  column_identifier: number = 1;

  // List of connected columns to allow dragging and dropping between columns
  connected_columns_list: string[] = [];

  // Boolean to keep track if we are dragging or clicking a fragment within the playground
  playground_dragging: boolean;

  // Variable to keep track of the window width, used to scale the site for small displays
  window_size: number;

  linnaeus_db = my_database
  linnaeus_array : object[] = []
  
  current_sandbox : Sandbox;
  current_content : any = '';
  current_animal_content : any = '';
  showFiller = false;

  index_table_columns: string[] = ['animal_name', 'id', 'category'];
  
  current_tab = 2
  activeNode:any;

  glossary_data_source = new MatTableDataSource();
  columnsToDisplay = ['glossary_name', 'taxon_href_id'];
  columnsToDisplayWithExpand = [...this.columnsToDisplay, 'expand'];
  expandedElement: object | null;

  index_table_data_source = new MatTableDataSource();
  
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  hide: boolean = true; // Whether to hide passwords in the material form fields

  // We only allow the delete fragment button if one is actually selected.
  fragment_selected: boolean = false;

  treeControl = new NestedTreeControl<taxon_node>(node => node.children);
  dataSource = new MatTreeNestedDataSource<taxon_node>();
  hasChild = (_: number, node: taxon_node) => !!node.children && node.children.length > 0;

  constructor(
    protected api: ApiService,
    protected utility: UtilityService,
		// protected auth_service: AuthService,
    // protected dialog: DialogService,
    private matdialog: MatDialog, 
    
    ) {

      this.dataSource.data = TREE_DATA;

     }

  ngOnInit(): void {
    // Retrieve the window_size to correctly set the navbar size



    // this.treeControl.expandDescendants(this.dataSource.data[0])

    this.current_sandbox = new Sandbox({})
    // let linneus_array : object[] = []

    for (let i in this.linnaeus_db){
      this.linnaeus_array.push(this.linnaeus_db[i])
    }
    
    // console.log('sandbox', this.linnaeus_array)

    this.request_sandbox('Aetideidae of the World Ocean')
    this.request_sandbox_content('Welcome')

    this.expand_tree_to_node('Aetideopsis albatrossae')
    this.load_animal_data('Aetideopsis albatrossae')
  }

  
  ngAfterViewInit() {
    this.index_table_data_source.paginator = this.paginator;
    this.index_table_data_source.sort = this.sort;
  }
  
  protected expand_tree_to_node(node_name: string): void {
    console.log('nodename', this.dataSource.data)
    let temp = this.dataSource.data.find(i => i['name'] === node_name);

    console.log('active', temp)
    
    this.treeControl.collapseAll();
    this.expand_tree(this.dataSource.data, node_name);
  }

  private expand_tree(data, node_name: string): any {
    
    data.forEach(node => {
      if (node.children && node.children.find(c => c.name === node_name)) {
                
        this.treeControl.expand(node);
        this.expand_tree(this.dataSource.data, node.name);
      }
      else if (node.children && node.children.find(c => c.children)) {
        this.expand_tree(node.children, node_name);
      }
    });
  }

  protected request_sandbox(sandbox_title){
    let item1 = this.linnaeus_array.find(i => i['title'] === sandbox_title);
    this.current_sandbox = new Sandbox(item1)

    console.log('current sandbox', this.current_sandbox)

    this.index_table_data_source = new MatTableDataSource(this.current_sandbox['index'])
    this.glossary_data_source = new MatTableDataSource(this.current_sandbox['glossary'])

  }

  protected request_sandbox_content(sandbox_content_title){
    let item1 = this.current_sandbox.introduction.find(i => i['title'] === sandbox_content_title);
    this.current_content = item1
  }

  protected applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.index_table_data_source.filter = filterValue.trim().toLowerCase();

    if (this.index_table_data_source.paginator) {
      this.index_table_data_source.paginator.firstPage();
    }
  }
  
  protected table_filter(filter_value): void {
    // if (filter_value == '') {

    // }
    
    const filterValue = filter_value;
    this.index_table_data_source.filter = filterValue.trim().toLowerCase();
  }

  protected load_animal_data(animal_name){
    this.current_animal_content = this.current_sandbox.animals.find(i => i['name'] === animal_name);
    // console.log(this.current_animal_content)
  }

  protected test(thing): void{
    // const filterValue = 'bat';
    // this.index_table_data_source.filter = filterValue.trim().toLowerCase();

    console.log('############ TESTING ############')
    console.log(this.activeNode)

    // console.log(thing);

    // let temp = 


    // console.log(this.glossary_data_source)
  }
}
