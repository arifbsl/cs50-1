#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    //lists variables used in program
    float Cash = 0;
    int Change = 0, Quarters = 0, Dimes = 0, Nickels = 0, Pennies = 0, Number_of_Coins = 0;

    do
    {
        Cash = get_float("Cash given in Dollars to convert to Change in Coins: ");
    }
    while (Cash <= 0);
    
    //converts dollars to cents
    Change = round(Cash * 100);
    
    //finds maximium number quarters that can be used
    Quarters = Quarters + Change / 25;
    
    //updates Change to reflect amount remaining
    Change = Change % 25;
    
    //finds maximium amount of dimes that can be used
    Dimes = Dimes + Change / 10;
    
    //updates Change to reflect amount remaining
    Change = Change % 10;
    
    //finds maximium amount of nickels that can be used
    Nickels = Nickels + Change / 5;
    
    //updates Change to reflect amount remaining
    Change = Change % 5;
    
    //finds maximium amount of pennies that can be used
    Pennies = Pennies + Change / 1;
    
    //updates Change to reflect amount remaining
    Change = Change % 1;
    
    //adds up total coins used 
    Number_of_Coins = Quarters + Dimes + Nickels + Pennies;

    //prints out number of each coin type given back
    printf("You were giving back %i Quarters, %i Dimes, %i Nickels, %i Pennies.\n", Quarters, Dimes, Nickels, Pennies);
    
    //prints out total number of coins given back
    printf("You recieved %i coins back.\n", Number_of_Coins);
}

