#include <iostream>
#include<bitset>
#include<vector>
#include<fstream>
int a=12;
int b=23;

int add(int a, int p){


    int k=34;

    return k+a-p;
}

int main(){


    // int c;
    // c=a+b;
    // std :: cout << c << "\n";
    // std :: cout << add(34,4) << "\n";
    
    // std :: cout << c;
    // std ::cin >> c;
    // std :: cout << c;
    // int t=10;
    // int &ref=t;
    // std :: cout << ref;


    // float a = 0.1;
    // float b = 0.2;
    // float c= 0.3;

    // if(a+b==c){

    //     std :: cout << "this work" << std :: ends;
    // }
    // else{

    //     std::cout << "not work" << std::ends;
    // }


    // int a=-2;
    // int b= a << 1;
    // std :: cout << std::bitset<16>(a) <<"\n" <<std ::ends;
    // std :: cout << a << "\n" << std :: ends;

    // std :: cout << std::bitset<8>(b) <<"\n" <<std ::ends;
    // std :: cout << b <<"\n" <<std :: ends;
    // b=b>>1;

    // std :: cout << std::bitset<8>(b) << "\n"<<std ::ends;
    // std:: cout << b << "\n"<<std:: ends;


    // int arr[6]={12,12,34,5,5,56};
    // int ar[]={12,34,45};

    // for(int i=0;i<=5;i++){

    //     std:: cout << arr[i] << "\n"<< std :: ends;




    // }




std::vector<int> v = { 1, 2, 3, 4, 5 };

for(auto val:v){

    std::cout << val << std:: ends;
}

std::ofstream os("foo.txt");
if(os.is_open()){
os << "Hello World!";
}



//intialize vector using an initializer_list
// for (std::vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
// std::cout << *it << " ";
// }



}

