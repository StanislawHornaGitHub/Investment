#!/bin/sh

Main (){
    LoadFunds
    CalcInvestments
}

LoadFunds(){

    # Start python script to load fund URLs
    python3 ./Worker/Load_Funds.py
}

CalcInvestments(){
    python3 ./Worker/Calculate_investment_results.py
}

Main