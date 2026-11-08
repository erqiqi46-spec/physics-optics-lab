import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'./tests',timeout:60000,workers:1,use:{baseURL:'http://localhost:5173',headless:true,viewport:{width:1440,height:1080},launchOptions:{args:['--no-sandbox','--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader']}},reporter:[['list'],['json',{outputFile:'evidence/browser-results.json'}]]});
