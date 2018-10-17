#include "msp430g2553.h"

void UARTSendArray(unsigned char * TxArray, unsigned char ArrayLength);

static volatile char data;

void main(void)
{
    WDTCTL = WDTPW | WDTHOLD;   // stop watchdog timer

    // Sets DCO to 1MHz (Family Users Guide)
    DCOCTL = 0;                 // Select lowest DCOx and MODx settings
    BCSCTL1 = CALBC1_1MHZ;      // Set range
    DCOCTL = CALDCO_1MHZ;       // Set DCO step + modulation

    // Port 1
    P1DIR = 0x00; // all inputs
    P1REN = 0xFF; // all on
    P1OUT = 0x00; // all pull down

    // Port 2
    P2DIR = 0xFF; // all outputs
    P2OUT = 0x00; // all low

    // Configure hardware UART
    P1SEL = BIT1 + BIT2;    // P1.1 = RXD, P1.2=TXD
    P1SEL2 = BIT1 + BIT2;   // P1.1 = RXD, P1.2=TXD
    UCA0CTL1 |= UCSSEL_2;   // Use SMCLK
    UCA0BR0 = 104;          // Set baud rate to 9600 with 1MHz clock (Data Sheet 15.3.13)
    UCA0BR1 = 0;            // Set baud rate to 9600 with 1MHz clock
    UCA0MCTL = UCBRS0;      // Modulation UCBRSx = 1
    UCA0CTL1 &= ~UCSWRST;   // Initialize USCI state machine
    IE2 |= UCA0RXIE;        // Enable USCI_A0 RX interrupt

    __bis_SR_register(LPM0_bits + GIE); // interrupts enabled and set to low power mode

    /*while(1){                                 // This while loop was originally written
        if ((P1IN & 0x01) == 0x01){             // to test the rover's motors using three (3)
            P2OUT |= 0x30; // Enable motors     // switches as inputs. It has been left here
        }                                       // for future troubleshooting purposes.
        else{
            P2OUT &= 0xCF; // Disable motors
        }
        if ((P1IN & 0x08) == 0x08){
            P2OUT |= 0x02; // Motor A Forward
            P2OUT &= 0xFE;
        }
        else{
            P2OUT |= 0x01; // Motor A Backward
            P2OUT &= 0xFD;
        }
        if ((P1IN & 0x10) == 0x10){
            P2OUT |= 0x04; // Motor B Forward
            P2OUT &= 0xF7;
        }
        else{
            P2OUT |= 0x08; // Motor B Backward
            P2OUT &= 0xFB;
        }
    }*/
}

/* This interrupt is triggered when the MSP430G2553(MCU) receives
 * data via UART communication. It is responsible for changing the
 * configuration of the motors to what has been requested. */
#pragma vector = USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void){
    data = UCA0RXBUF;

    switch (data) {
    case 'w':{
        P2OUT &= 0xCF; // Disable motors
        P2OUT |= 0x02; // Motor A Forward
        P2OUT &= 0xFE;
        P2OUT |= 0x04; // Motor B Forward
        P2OUT &= 0xF7;
        P2OUT |= 0x30; // Enable motors
    }
    break;
    case 'a':{
        P2OUT &= 0xCF; // Disable motors
        P2OUT |= 0x02; // Motor A Forward
        P2OUT &= 0xFE;
        P2OUT |= 0x08; // Motor B Backward
        P2OUT &= 0xFB;
        P2OUT |= 0x30; // Enable motors
    }
    break;
    case 's':{
        P2OUT &= 0xCF; // Disable motors
        P2OUT |= 0x01; // Motor A Backward
        P2OUT &= 0xFD;
        P2OUT |= 0x08; // Motor B Backward
        P2OUT &= 0xFB;
        P2OUT |= 0x30; // Enable motors
    }
    break;
    case 'd':{
        P2OUT &= 0xCF; // Disable motors
        P2OUT |= 0x01; // Motor A Backward
        P2OUT &= 0xFD;
        P2OUT |= 0x04; // Motor B Forward
        P2OUT &= 0xF7;
        P2OUT |= 0x30; // Enable motors
    }
    break;
    case 'x':{
        P2OUT &= 0xCF; // Disable motors
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
