#include <iostream>
#include <cassert>
#include <fstream>

#include "thulac.h"
#include "nlohmann/json.hpp"
#include "indicators/progress_bar.hpp"

using std::cin;
using std::cout;
using std::endl;

void showhelp(){
    std::cerr<<"Command line usage:"<<std::endl;
    std::cerr<<"./thulac [-t2s] [-seg_only] [-filter] [-deli delimeter] [-user userword.txt] [-model_dir dir]"<<std::endl;
    std::cerr<<"or"<<std::endl;
    std::cerr<<"./thulac [-t2s] [-seg_only] [-filter] [-deli delimeter] [-user userword.txt] [-intput inputfile] [-output outputfile]"<<std::endl;
    std::cerr<<"\t-t2s\t\t\ttransfer traditional Chinese text to Simplifed Chinese text"<<std::endl;
    std::cerr<<"\t-seg_only\t\tsegment text without Part-of-Speech"<<std::endl;
    std::cerr<<"\t-filter\t\t\tuse filter to remove the words that have no much sense, like \"could\""<<std::endl;
    std::cerr<<"\t-deli delimeter\t\tagsign delimeter between words and POS tags. Default is _"<<std::endl;
    std::cerr<<"\t-user userword.txt\tUse the words in the userword.txt as a dictionary and the words will labled as \"uw\""<<std::endl;
    std::cerr<<"\t-model_dir dir\t\tdir is the directory that containts all the model file. Default is \"models/\""<<std::endl;
    std::cerr<<"\t-input inputfile\t\tinputfile is the text that needs to be segmented. Default is stdin"<<std::endl;
    std::cerr<<"\t-output outputfile\t\toutputfile is the result of the output. Default is stdout"<<std::endl;
}

int main (int argc,char **argv) {

    char* user_specified_dict_name=NULL;
    char* model_path_char = NULL;
    char* input_path = NULL;
    char* output_path = NULL;


    char separator = '_';

    bool useT2S = false;
    bool seg_only = false;
    bool useFilter = false;
    bool multi_thread = false;

    int c = 1;
    while(c < argc){
        std::string arg = argv[c];
        if(arg == "-t2s"){
            useT2S = true;
        }else if(arg == "-user"){
            user_specified_dict_name = argv[++c];
        }else if(arg == "-deli"){
            separator = argv[++c][0];
        }else if(arg == "-seg_only"){
            seg_only = true;
        }else if(arg == "-filter"){
            useFilter = true;
        }else if(arg == "-model_dir"){
            model_path_char = argv[++c];
        }else if(arg == "-input") {
            input_path = argv[++c];
        }else if(arg == "-output") {
            output_path = argv[++c];
        }else if(arg == "-multi-thread") {
            multi_thread = true;
        }else{
            showhelp();
            return 1;
        }
        c ++;
    }

    THULAC lac;
    lac.init(model_path_char, user_specified_dict_name, seg_only, useT2S, useFilter);
    std::ifstream finput;
    if(input_path) {
        finput.open(input_path);
        cin.rdbuf(finput.rdbuf());
    }
    std::ofstream foutput;
    if(output_path) {
        foutput.open(output_path);
        cout.rdbuf(foutput.rdbuf());
    }
    std::string raw;
    THULAC_result result;
    clock_t start = clock();
    std::vector<std::string> raws;
    while (getline(cin, raw)) raws.push_back(raw);
    using namespace indicators;
    int mod = 5000;
    ProgressBar bar{
        option::BarWidth{50},
        option::Start{"["},
        option::Fill{"="},
        option::Lead{">"},
        option::Remainder{" "},
        option::End{"]"},
        option::PostfixText{"cutting"},
        option::ForegroundColor{Color::green},
        option::FontStyles{std::vector<FontStyle>{FontStyle::bold}},
        option::MaxProgress{raws.size() / mod},
        option::ShowPercentage{true},
        option::ShowElapsedTime{true},
        option::ShowRemainingTime{true},
    };

    int cnt = 0;
    for (const auto &raw: raws) {
        lac.cut(raw, result);
        std::vector<std::string> tokens;
        for (const auto &[word, pos]: result) {
            tokens.push_back(word);
            tokens.push_back(word + std::string(1, separator) + pos);
        }
        cnt++;
        if (cnt % mod == 0) bar.tick();
    }
    clock_t end = clock();
    double duration = (double)(end - start) / CLOCKS_PER_SEC;
    std::cerr<<duration<<" seconds"<<std::endl;
    finput.close();
    foutput.close();
    return 0;
}
