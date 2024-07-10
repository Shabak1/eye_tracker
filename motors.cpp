// задаем имена для портов
#define IN1 4
#define IN2 5
#define IN3 6
#define IN4 7

void setup() {
   pinMode(IN1, OUTPUT);
   pinMode(IN2, OUTPUT);
   pinMode(IN3, OUTPUT);
   pinMode(IN4, OUTPUT);
   Serial.begin(9600);
}

void loop() {
   if (Serial.available() > 0) {
      char command = Serial.read();
      switch (command) {
         case 'F': // Едем вперед
            digitalWrite(IN1, HIGH);
            digitalWrite(IN2, LOW);
            digitalWrite(IN3, HIGH);
            digitalWrite(IN4, LOW);
            break;
         case 'B': // Едем назад
            digitalWrite(IN1, LOW);
            digitalWrite(IN2, HIGH);
            digitalWrite(IN3, LOW);
            digitalWrite(IN4, HIGH);
            break;
         case 'L': // Поворот налево
            digitalWrite(IN1, LOW);
            digitalWrite(IN2, LOW);
            digitalWrite(IN3, HIGH);
            digitalWrite(IN4, LOW);
            break;
         case 'R': // Поворот направо
            digitalWrite(IN1, HIGH);
            digitalWrite(IN2, LOW);
            digitalWrite(IN3, LOW);
            digitalWrite(IN4, LOW);
            break;
         case 'S': // Остановка
            digitalWrite(IN1, LOW);
            digitalWrite(IN2, LOW);
            digitalWrite(IN3, LOW);
            digitalWrite(IN4, LOW);
            break;
      }
   }
}
