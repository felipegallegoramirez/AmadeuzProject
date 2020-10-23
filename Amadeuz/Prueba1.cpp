#include <iostream>
#include <windows.h>
#include<stdlib.h>
#include<time.h>
#include<fstream>//Para ficheros
using namespace std;

int main(){
    // parte simulacion
        srand(time(NULL));
        ofstream fs("posibilidades.csv");
        ofstream fa("camino.csv");

int valores[13],tru[5],multi[5];

fs<<"Tamano1 , velocidad1 , distancia1 ,Tamano2 , velocidad2 , distancia2 , Tamano3 , velocidad3 , distancia3 , Tamano4 , velocidad4 , distancia4"<<endl;
fa<<"Camino"<<endl;

for(int i=0;i<=1000000;i++){
        int f=0;
f=1 + rand() % (100 +1 - 1) ;
        for(int r=0;r<=9;r=r+3){

    valores[r]=1 + rand() % (1000 +1 - 1) ;
    valores[r+1]=1 + rand() % (80 +1 - 1) ;
    if((1+rand() % (3 +1 - 1))!=2){
    valores[r+2]=f+1 ;
    }else{valores[r+2]=f-1;}

    if(valores[r+2]<f){

                tru[r/3]=1;
                multi[r/3]=valores[r]/valores[r+1];
             }else{tru[r/3]=0;}
        }
                for (int x=0;x<=4;x++ ){
                if(tru[x]==1){
       for (int y=0;y<=4;y++ ){

                if(tru[y]==1){
                    if(multi[y]<multi[x]){
                        tru[x]=0;
                    }}}}
        }
        bool unico=false;
       for (int x=0;x<=4;x++ ){
            if(unico==false){
      if(tru[x]==1){
            unico=true;
}
            }else{ if(tru[x]==1){
            unico=false;
            break;}
            }
       }
bool entro=false;
        if (unico=true){


        if(tru[0]==1){
entro=true;
            fa<<0<<endl;
        }else if(tru[1]==1){
            entro=true;
        fa<<1<<endl;
        }else if(tru[2]==1){
            entro=true;
        fa<<2<<endl;
        }else if(tru[3]==1){
            entro=true;
        fa<<3<<endl;
        }
        if(entro==true){fs<<valores[0]<<" , "<<valores[1]<<" , "<<valores[2]<<" , "<<valores[3]<<" , "<<valores[4]<<" , "<<valores[5]<<" , "<<valores[6]<<" , "<<valores[7]<<" , "
        <<valores[8]<<" , "<<valores[9]<<" , "<<valores[10]<<" , "<<valores[11]<<endl;}



        }
      //  fa<<tru[0]<<" , "<<tru[1]<<" , "<<tru[2]<<" , "<<tru[3]<<" , "<<endl;
        }
tru[1]=0;
tru[2]=0;
tru[3]=0;
tru[0]=0;
/*
        */




fs.close();
fa.close();
}
