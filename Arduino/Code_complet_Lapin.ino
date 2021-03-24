//*************************************************************************************************
//
//                                    Code complet Lapin automate
//
//*************************************************************************************************


int enable_pin = 2; //Pin d'activation du compresseur
int dir_pin = 22;   //Pin de durction du compresseur
int valve_pin = 8;  //Pin de commande de l'électrovanne

boolean readFromSerial; //Booléen pour autoriser la lecture des données depuis Serial

//Pour la séquence d'inspiration
boolean inspi = 0; //Détermine si le lapin doit inspirer ou pas
double fan_voltage = 0; //Tension à fournir au ventilateur

//Fréquences obtenues par la génération de données
double frequence_cardiaque;
double frequence_respiratoire;

//Traduction des fréquences en périodes utilisables ici
double periodeBattements = 100000;
double periodeRespi = 100000;
int dureeBattement = 10;

//Lecture depuis Serial
boolean choixFrequence;
int ser;
String frequence_cardiaque_lue;
String frequence_respi_lue;

double pourcentage;


void setup() {
  Serial.begin(9600); //Initialisation de Serial
  pinMode(enable_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);
  pinMode(valve_pin, OUTPUT);
  pinMode(A7,OUTPUT); //pin du moteur haptique (fréquence cardiaque)
  digitalWrite(dir_pin,LOW); //on impose la direction à 0 (pas de changement de direction ici)

  pinMode(A6,OUTPUT);

  //Interruption
  cli(); // Désactive l'interruption globale
  bitClear (TCCR2A, WGM20); // WGM20 = 0
  bitClear (TCCR2A, WGM21); // WGM21 = 0 
  TCCR2B = 0b00000110; // Clock / 256 soit 16 micro-s et WGM22 = 0
  TIMSK2 = 0b00000001; // Interruption locale autorisée par TOIE2
  sei(); // Active l'interruption globale

  readFromSerial = 0; //Ne passe à 1 que lors de l'interruption


}

int varCompteur = 0; // La variable compteur pour l'interruption

int varCompteurEntreBattements = 0; //Interruption pour contrôler le moteur haptique

int varCompteurRespi = 0; //Interruption pour contrôler la respiration



// Routine d'interruption
ISR(TIMER2_OVF_vect) 
{
  TCNT2 = 256 - 248; // 250 x 16 µS = 4 ms
  if (varCompteur++ > 125*2) 
  { 
    // 125 * 2 * 4 ms = 1000 ms
    varCompteur = 0;



    
    // Autorisation lecture fréquences
    //readFromSerial = 1; 
  }
  if (varCompteurEntreBattements++ == int(periodeBattements - dureeBattement) )
  {
    //varCompteurEntreBattements = 0;
    //Serial.println("Coeur on");
    analogWrite(A7,150);
    analogWrite(A6,150);
  }
  if (varCompteurEntreBattements > periodeBattements )
  {
    varCompteurEntreBattements = 0;
    //Serial.println("Coeur off");
    analogWrite(A7,0);
    analogWrite(A6,0);
  }



  if (varCompteurRespi++ == int(periodeRespi/2))
  {
    Serial.println("Expiration");
    analogWrite(enable_pin,0);
    analogWrite(valve_pin,255); //On ouvre l'électrovanne pour laisser échapper l'air
    inspi = 0; //On termine la séquence d'inspiration
    fan_voltage = 0;
    
  }
  if (varCompteurRespi > periodeRespi)
  {
    Serial.println("Inspiration");
    inspi = 1; //On déclenche la séquence d'inspiration
    analogWrite(valve_pin,0); //On ferme l'électrovanne pour gonfler le poumon
    varCompteurRespi = 0;
  }

  if ((inspi == 1) && (fan_voltage < 255))
  {
    fan_voltage += 255.0/((1.0/3)*periodeRespi); //Calcul de la quantité à incrémenter la tension toutes les 4 ms pour obtenir un gonflement doux
    analogWrite(enable_pin,fan_voltage);
  }
}

void loop() {
  choixFrequence = 0;
  frequence_cardiaque_lue = "";
  frequence_respi_lue = "";
  //analogWrite(A6,150);
  if (Serial.available() > 0){
    do{
      ser = Serial.read();
      //Serial.println(ser);
      if (char(ser)=='c'){choixFrequence = 1;}
      else if (ser != -1){
        if (choixFrequence == 0){
          frequence_cardiaque_lue += char(ser);
          
        }
        else if (char(ser) != 'r'){
          frequence_respi_lue += char(ser);
          //analogWrite(A6,0);
          
        }
      }
    }while (char(ser) != 'r');
  }
  if (frequence_cardiaque_lue != ""){
    frequence_cardiaque = frequence_cardiaque_lue.toDouble();
    frequence_respiratoire = frequence_respi_lue.toDouble();
    Serial.print(frequence_cardiaque_lue);
    Serial.print(";");
    Serial.println(frequence_respi_lue);
    Serial.print(frequence_cardiaque);
    Serial.print(";");
    Serial.println(frequence_respiratoire);

    periodeBattements = (60*1000.0)/(4*frequence_cardiaque);

    pourcentage = double(varCompteurRespi)/periodeRespi;
    Serial.println(pourcentage);
    periodeRespi = (60*1000.0)/(4*frequence_respiratoire);
  }
  
  
  //if (readFromSerial){
    //lecture depuis Serial
    

    
    //frequence_cardiaque = 100; //en battements/minute
    //frequence_respiratoire = 30; //en repirations/minute

    //periodeBattements = (60*1000.0)/(4*frequence_cardiaque);
    //periodeRespi = (60*1000.0)/(4*frequence_respiratoire);
    //readFromSerial = 0;
    
  //}


}
