#include <IRremote.h>
#define RAW 11

int IR_RECV_PIN = D4;
int IR_RECV_ENABLE_PIN = D6;
int IR_SEND_PIN = A5;

IRrecv ir_recv(IR_RECV_PIN);
IRsend ir_send; // Send pin A5 hard coded in IRRemoteInt.h
decode_results ir_recv_code;

int getIR(String command);

String getIR_data = "";

void setup() {
    // Set pin modes
    pinMode(IR_RECV_PIN, OUTPUT);
    pinMode(IR_RECV_ENABLE_PIN, OUTPUT);
    
    // Create cloud functions
    Particle.function("getIR", getIR);
    Particle.function("getIR_Cancel", getIR_Cancel);
    Particle.function("sendIR", sendIR);
    Particle.variable("getIR_data", getIR_data);
}

void loop() {
    // Get IR code if enabled
    if (IR_RECV_ENABLE_PIN) {
        if (ir_recv.decode(&ir_recv_code)) {
            digitalWrite(IR_RECV_ENABLE_PIN, LOW);
            char buf[20];
            int n;
            if (ir_recv_code.decode_type == PANASONIC)
            {
                n = sprintf(buf, "%d,%d,%d", ir_recv_code.decode_type, ir_recv_code.panasonicAddress, ir_recv_code.value);
            }
            else
            {
                n = sprintf(buf, "%d,%d,%d", ir_recv_code.decode_type, ir_recv_code.value, ir_recv_code.bits);
            }
            getIR_data = String(buf, n);
        }
    }
}

int getIR(String notUsed) {
    // Enable IR receiever
    getIR_data = "";
    digitalWrite(IR_RECV_ENABLE_PIN, HIGH);
    ir_recv.enableIRIn();
}

int getIR_Cancel(String notUsed) {
    // Disable IR receiever
    digitalWrite(IR_RECV_ENABLE_PIN, LOW);
}

int sendIR(String data) {
    int args[3];
    const char* buf = data.c_str();
    char* arg = strtok(strdup(buf), ",");
    for (int i = 0; i < 3; i++) {
        args[i] = atoi(arg);
        arg = strtok(NULL, ",");
    }
    switch (args[0]) {
        case NEC:
            ir_send.sendNEC(args[1], args[2]);
            break;
        case SONY:
            ir_send.sendSony(args[1], args[2]);
            break;
        case RC5:
            ir_send.sendRC5(args[1], args[2]);
            break;
        case RC6:
            ir_send.sendRC6(args[1], args[2]);
            break;
        case SHARP:
            ir_send.sendSharp(args[1], args[2]);
            break;
        case PANASONIC:
            ir_send.sendPanasonic(args[1], args[2]);
            break;
        case JVC:
            ir_send.sendJVC(args[1], args[2], 0);
            break;
        case RAW:
            ir_send.sendSony(args[1], args[2], 38);
            break;
    }   
}