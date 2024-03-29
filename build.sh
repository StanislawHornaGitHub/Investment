#!/bin/sh


Main (){
    StartPostgresContainer
    LoadFunds
    LoadInvestments
    CalcInvestments
}

StartPostgresContainer(){
    
    # Set postgres directory, 
    # because in the startup script docker build is using current directory
    cd "./PostgreSQL" || exit 1

    # Start script to build docker image and start container
    ./rebuild.sh || exit 2

    # Go back to root directory
    cd "$(git rev-parse --show-toplevel)" || exit 1
}

LoadFunds(){

    # Start python script to load fund URLs
    python3 ./Flask/Worker/Load_Funds.py
}

LoadInvestments(){

    
    python3 ./Flask/Worker/Load_investment_config.py
}

CalcInvestments(){
    python3 ./Flask/Worker/Calculate_investment_results.py
}


Main