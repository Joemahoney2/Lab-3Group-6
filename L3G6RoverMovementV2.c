/******************************************
 * Lab 3 Group 6 Rover MCU code
 * Members: Adam Harper, Celina Luckevich
 *          Joseph Mahoney, Joshua Warren
 *
 * Pin Assignment
 *  P1:             P2:
 *      1.0 - MAG       2.0 - US1
 *      1.1 - RX        2.1 - ENA
 *      1.2 - TX        2.2 - ENB
 *      1.3 - PS        2.3 - US2
 *      1.4 -           2.4 - TRIG
 *      1.5 - SV1       2.5 - US3
 *      1.6 - SV2       2.6 - ADIR
 *      1.7 -           2.7 - BDIR
 *
 * Ultra Sonic:     (?)
 *  10us pulse for trigger
 *  distance (cm) = us/58
 *  1000cc = 1000us
 *  1000us/58 = 17.2cm range
 *  cut off set for 5 cm
 *  5cm*58us = 290us = 290cc
 *  goes into avoidance mode if signal gets back in 290cc or less
 *
 * Motors:
 *  min duty cycle of 30%
 *  1khs PWM = 1000us = 1000cc
 *  30%*1000 = 300cc
 *  duty cycle from 300cc to 1000cc
 *
 * Servos:
 *  20ms PWM signal
 *  1.5ms neutral
 *  20ms = 20000us = 20000cc
 *  1ms = 1000us = 1000cc
 *  2ms = 2000us = 2000cc
 *  duty cycle from 1000cc to 2000cc
 *****************************************/
#include "msp430g2553.h"

void UARTSendArray(unsigned char * TxArray, unsigned char ArrayLength);

static volatile char data;

int flag = 0;

int bump = 0;

long int i = 0;

void wait(long int cycles){
    for(i = 0; i < cycles; i++){}
}

void main(void)
{
    WDTCTL = WDTPW | WDTHOLD;   // stop watchdog timer

    // Sets DCO to 1MHz (Family Users Guide)
    DCOCTL = 0;                 // Select lowest DCOx and MODx settings
    BCSCTL1 = CALBC1_1MHZ;      // Set range
    DCOCTL = CALDCO_1MHZ;       // Set DCO step + modulation

    // TimerA0
    TA0CTL = TASSEL_2 + MC_1; // SMCLK, Up mode
    TA0CCTL0 = CCIE;    // Reset/Set
    TA0CCTL1 = CCIE;    // Reset/Set
    TA0CCTL2 = CCIE;    // Reset/Set
    TA0CCR0 = 20000;        // 20ms     servo period    50Hz
    TA0CCR1 = 2800;         // 2ms      sv1 pwm
    TA0CCR2 = 500;         // 1.5ms    sv2 pwm

    // TimerA1
    TA1CTL = TASSEL_2 + MC_1; // SMCLK, Up mode
    TA1CCTL0 = OUTMOD_7;    // Reset/Set
    TA1CCTL1 = OUTMOD_7;    // Reset/Set
    //TA1CCTL2 = OUTMOD_7;    // Reset/Set
    TA1CCR0 = 1000;         // 1ms      motor period    1kHz
    TA1CCR1 = 500;          // 500us    motor pwm
    //TA1CCR2 = 10;           // 10us     us pwm

    // PORT 1
    P1DIR |= 0xF5;  // 1.0,1.2,1.4-1.7 output
    P1OUT = 0x00;

    // PORT 2
    P2SEL &= 0x00;
    P2SEL |= 0x06; // 2.1,2.2 PWM
    P2SEL2 &= 0x00;
    P2DIR |= 0xD6; // 2.1,2.2,2.4,2.6,2.7 outputs
    P2REN |= 0x29;
    P2IE |= 0x29;
    P2OUT = 0x00;

    // Configure hardware UART
    P1SEL |= BIT1 + BIT2;    // P1.1 = RXD, P1.2=TXD
    P1SEL2 |= BIT1 + BIT2;   // P1.1 = RXD, P1.2=TXD
    UCA0CTL1 |= UCSSEL_2;   // Use SMCLK
    UCA0BR0 = 104;          // Set baud rate to 9600 with 1MHz clock (Data Sheet 15.3.13)
    UCA0BR1 = 0;            // Set baud rate to 9600 with 1MHz clock
    UCA0MCTL = UCBRS0;      // Modulation UCBRSx = 1
    UCA0CTL1 &= ~UCSWRST;   // Initialize USCI state machine
    IE2 |= UCA0RXIE;        // Enable USCI_A0 RX interrupt

    __bis_SR_register(GIE); // interrupts enabled
    while(1){
        if(flag){
            TA0CCR1 = 500;          // arm: deg0
            wait(150000); // wait 1.5 sec
            TA0CCR2 = 2100;         // claw: deg145
            wait(150000); // wait 1.5 sec
            TA0CCR1 = 2500;         // arm: deg180
            wait(150000); // wait 1.5 sec
            TA0CCR2 = 500;          // claw: deg0
            wait(150000); // wait 1.5 sec
            flag = 0;
            IE2 |= UCA0RXIE;        // Enable USCI_A0 RX interrupt
            P2IE |= 0x20;
        }
    }
}

void director(long int dir){
    TA1CCTL1 = 0;
    P2OUT &= 0x3F;
    P2OUT |= dir;
    TA1CCTL1 = OUTMOD_7;
}

#pragma vector=PORT2_VECTOR
__interrupt void Port2_ISR()
{
    IE2 &= ~UCA0RXIE;       // Disable USCI_A0 RX interrupt
    P2IE &= ~0x20;
    if(bump < 5){
        bump++;
    }
    // Hit something in front, go backward and turn right
    else if(P2IFG & BIT0){
        director(0x00);
        wait(110000);
        director(0x80);
        wait(110000);
        director(0xC0);
        bump = 0;
    }
    // Hit something on left, turn right
    else if(P2IFG & BIT3){
        director(0x80);
        wait(110000);
        director(0xC0);
        bump = 0;
    }
    // Hit something on right, turn left
    else if(P2IFG & BIT5){
        director(0x40);
        wait(110000);
        director(0xC0);
        bump = 0;
    }
    P2IE |= 0x20;
    IE2 |= UCA0RXIE;        // Enable USCI_A0 RX interrupt
    P2IFG = 0;
}

// Timer 0 A0 interrupt service routine
#pragma vector = TIMER0_A0_VECTOR
__interrupt void Timer0_A0_ISR( void ){
    P1OUT |= 0x60;
}

// Timer 0 A1 interrupt service routine
#pragma vector = TIMER0_A1_VECTOR
__interrupt void Timer0_A1_ISR( void ){
    switch( TA0IV ){
        case 2:{ // TA0CCR1
            P1OUT &= ~0x20;
            break;
        }
        case 4:{ // TA0CCR2
            P1OUT &= ~0x40;
            break;
        }
        case 10:{ // TA0IFG
            break;
        }
    }
}

/* This interrupt is triggered when the MSP430G2553(MCU) receives
 * data via UART communication. It is responsible for changing the
 * configuration of the motors to what has been requested. */
#pragma vector = USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void){
    data = UCA0RXBUF;

    switch (data) {
    case 'w':{
        director(0xC0);
    }
    break;
    case 'a':{
        director(0x40);
    }
    break;
    case 's':{
        director(0x00);
    }
    break;
    case 'd':{
        director(0x80);
    }
    break;
    case 'f':{
        IE2 &= ~UCA0RXIE; // Disable USCI_A0 RX interrupt
        P2IE &= ~0x20; // Disable P2 Interrupts
        TA1CCTL1 = 0; // Disable Motors
        flag = 1;
    }
    break;
    case 'x':{
        TA1CCTL1 = 0;
    }
    break;
    default:{
        UARTSendArray("ERROR: Command not found", 24);  // Used for testing purposes
        UARTSendArray("\n\r", 2);
    }
    break;
    }
}

/* Function used for sending data back to the terminal
 * through UART communication*/
void UARTSendArray(unsigned char * TxArray, unsigned char ArrayLength) {
  while (ArrayLength--) {
    while (!(IFG2 & UCA0TXIFG));
    UCA0TXBUF = * TxArray;
    TxArray++;
  }
}
