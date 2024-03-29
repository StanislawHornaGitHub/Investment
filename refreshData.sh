#!/bin/sh

Main (){
    LoadFunds
    CalcInvestments
}

LoadFunds(){

    # Start python script to load fund URLs
    python3 ./Flask/Worker/Load_Funds.py
}

CalcInvestments(){
    python3 ./Flask/Worker/Calculate_investment_results.py
}

Main