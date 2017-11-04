#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<fcntl.h>
#include<string.h>
#include <signal.h>
#include <iostream>

using namespace std;

string streetName[100]={""};
string sName="";

void sigtermHandler(int signum)
{
    signal(SIGTERM, SIG_DFL);
    exit(EXIT_FAILURE);
}


bool streetNamecheck( string str, int sno)
{
    for(int i=0;i<sno;i++)
    {
        if(streetName[i]==str)
        {return true;}

    }
    return false;
}



int check(int p1[],int p2[],int p3[],int p4[]){
    float a,b,c,d;
    float a1,c1;
    float x1=(float)p1[0], x2=(float)p2[0],x3=(float)p3[0], x4=(float)p4[0];
    float y1=(float)p1[1], y2=(float)p2[1], y3=(float)p3[1], y4=(float)p4[1];

    if((x3 == x4) && (y3 == y4)){
        return 0;
    }

    if(((x1 == x3) && (y1 == y3) && (x2 == x4) && (y2 == y4))
       ||((x1 == x4) && (y1 == y4) && (x2 == x3) && (y2 == y3))){
        return 0;
    }

    if((x1 == x2) && (x1 == x3) && (x1 == x4)){
        if(((y1<y3)<y2) || ((y2<y3)<y1) || ((y1<y4)<y2) || ((y2<y4)<y1)
           || ((y3<y1)<y4) || ((y4<y1)<y3) || ((y3<y2)<y4) || ((y4<y2)<y3)){
            return 0;
        }
    }
    else{
        a1=(x1 - x2);
        c1=(x3 - x4);
        if(a1!=0 && c1!=0){
            a = (y1 - y2)/a1;
            b = y1 - a * x1;
            c = (y3 - y4)/c1;
            d = y3 - c * x3;
            if(a==0.0 && c==0.0){
                if((((x1<x3)<x2) || ((x2<x3)<x1) || ((x1<x4)<x2) || ((x2<x4)<x1)
                    || ((x3<x1)<x4) || ((x4<x1)<x3) || ((x3<x2)<x4) || ((x4<x2)<x3))){
                    return 0;
                }
            }
            else if(a==c){
                if(y3==a*x3+b &&
                   (((y1<y3)<y2) || ((y2<y3)<y1) || ((y1<y4)<y2) || ((y2<y4)<y1)
                    || ((y3<y1)<y4) || ((y4<y1)<y3) || ((y3<y2)<y4) || ((y4<y2)<y3))){
                    return 0;
                }
            }
        }
    }
    return 1;
}


int RandomPoint(int min,int max){
    int result;
    static int fd =-1;
    char *next_random_byte;
    int bytes_to_read;
    unsigned random_value;

    if (fd == -1){
        fd =open("/dev/urandom",O_RDONLY);
    }
    next_random_byte =(char*)&random_value;
    bytes_to_read = sizeof(random_value);
    do{
        int bytes_read;
        bytes_read = read(fd,next_random_byte,bytes_to_read);
        bytes_to_read -=bytes_read;
        next_random_byte +=bytes_read;
    }while(bytes_to_read>0);

    result =min+ (random_value %(max-min+1));
return result;
}






string randomstreet(int StreetNo)
{  int len;
    char c;

    for (int k=0;k<100;k++)
    {streetName[k]="";}

    for(int i=0;i<StreetNo;i++)
    {
        do{
            len=RandomPoint(1,25);
            sName="";
            for (int j=0;j<len;j++)
            { c=RandomPoint(65,90);
                sName+=c;
            }
        } while(streetNamecheck(sName,StreetNo));
        streetName[i]=sName;
        sName="";
    }

}

void AddRemoveandG(int street[100][500][2],int sn,int count[100],int remove){
    
    int j,k;
   
    for(j=0;j<remove;j++){

        cout<<"r "<<"\""<<streetName[j]<<"\""<<"\n";
    }

    char c;
    int len;
    for (int k=0;k<100;k++)
    {streetName[k]="";}

    for(int i=0;i<sn;i++)
    {
        do{
            len=RandomPoint(1,25);
            sName="";
            for (int j=0;j<len;j++)
            { c=RandomPoint(65,90);
                sName+=c;
            }
        } while(streetNamecheck(sName,sn));
        streetName[i]=sName;
        sName="";
    }

    for(j=0;j<sn;j++){

        cout<<"a "<<"\""<<streetName[j]<<"\"";
        for(k=0;k<count[j];k++){

            cout<<"("<<street[j][k][0]<<","<<street[j][k][1]<<")";
        }

        cout<<"\n";
    }
   
    cout<<"g\n";
}

void initcount(int count[100]){
    int i;
    for (i = 0; i < 100; i++){
        count[i]=0;
    }
}

int main(int argc,char* argv[]){
    
    int StreetNoMax=10,StreetNoMin=2; // [2,k]
    int LineMax=5, LineMin=1; //[1,k]

    int secondmax=5; //[5,k]
    int pointmax=20; //[-k,k]

    int sn,sl,second,pointX,pointY;
    int street[100][500][2]={0};

    int i,j,k;
    int m,n,t;

    int error=0;
    int temp[2];
    int checkresult;
    int count[100]={0};
    int remove=0;

    if(argc>1){

        int param;
        for(i=1;i<argc-1;i++){
            param = atoi(argv[i+1]);
            if(strcmp(argv[i],"-s")==0){
                if(param<2){
                    fprintf(stderr,"Error: Streets should not be less than 2\n");
                    return 0;
                }else{
                    StreetNoMax = param;
                }
            }
            else if(strcmp(argv[i],"-n")==0){
                if(param<1){
                    fprintf(stderr,"Error: Line Segment cannot be less than 1\n");
                    return 0;
                }else{
                    LineMax = param;
                }
            }
            else if(strcmp(argv[i],"-l")==0){
                if(param<5){
                    fprintf(stderr,"Error: Timer  should not be less than 5\n");
                    return 0;
                }else{
                    secondmax = param;
                }
            }
            else if(strcmp(argv[i],"-c")==0){
    if(param==0){
                    fprintf(stderr,"Error: Coordinates should not be 0\n");
                    return 0;
                }else{
                    pointmax = param;
                }
                
            }
        }
    }


    second = RandomPoint(5,secondmax);
    signal(SIGTERM, sigtermHandler);
    while(1){
        sn = RandomPoint(StreetNoMin, StreetNoMax);
        j=0;//street number
        initcount(count);
        error = 0;
        while(j<sn){
            sl = RandomPoint(LineMin+1,LineMax+1);
            k=0;//street point
            while(k<sl){
                if (error>=25){
                    fprintf(stderr,"Error: Number of Random generated excedded 25 times\n");
                    return 0;
                }
                pointX = RandomPoint(-pointmax,pointmax);
                pointY = RandomPoint(-pointmax,pointmax);
                temp[0]=pointX;
                temp[1]=pointY;

                //same point
                if(k>0){
                    if(street[j][k-1][0]==temp[0] && street[j][k-1][1]==temp[1]){
                        error++;
                        continue;
                    }
                }


                //self
                for(n=0;n<k-1&&k>0;n++){
                    checkresult = check(street[j][n],street[j][n+1],street[j][k-1],temp);
                    if(checkresult == 0){
                        error++;
                        break;
                    }
                }
                //self wrong no k++
                if(n<k-1&&k>0){
                    continue;
                }

                //other
                t=0;
                for(m=0;m<j&&k>0;m++){
                    for(n=0;n<count[t]-1;n++){
                        checkresult = check(street[m][n],street[m][n+1],street[j][k-1],temp);
                        if(checkresult == 0){
                            error++;
                            break;
                        }
                    }
                    //other wrong no k++
                    if(n<count[t]-1){
                        break;
                    }
                    t++;
                }
                //other wrong no k++
                if(m<j&&k>0){
                    continue;
                }

                street[j][k][0]=pointX;
                street[j][k][1]=pointY;
                count[j]++;
                k++;
            }
            j++;
        }

        AddRemoveandG(street,sn,count,remove);
        fflush(stdout);
        usleep(second*1000000);
        remove = sn;
    }
    return 0;
}

