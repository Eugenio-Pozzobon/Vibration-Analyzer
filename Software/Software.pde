import org.gicentre.utils.gui.TextPopup;
import java.util.Random;

// Sketch to show how a text popup window can be added to a sketch
// Version 1.3, 6th February, 2016.
// Author Jo Wood, giCentre.

// ------------------ Sketch-wide variables --------------------

private TextPopup textPopup;

//-----------------------------------------------------------------
import processing.serial.*; //Biblioteca importante para essa aplicação
Serial mySerial; //Funcionalidade serial

//configuração dos aruqivos logs e seu número máximo
int tela=0;
PrintWriter log; //arquivo do cabeçalho do arduino

//imagens usadas
PImage formulaLogo;
PImage ufsmLogo;
PImage steeringImage;

String cabecalho; //dados do cabeçalho na inicialização do arduino
boolean  cabecalhob=false; //informa se um cabeçalho de arquivo novo foi lido ou não
int linhaDados=0;// conta o número de linha de dados
int lastValue=0; //último valor recebido no buffer

int numValues=50; //número de valores separados nas linhas da tabela
String[] values=new String[numValues];
int logs=0; //log atual em gravação

void setup() {
  //size(1800, 900);
  fullScreen(P3D,2);
  background(255);
  frameRate(60);
  //cria o arquivo de cabeçalho do programa
  log = createWriter("log.csv");
}

void draw() { //Configura a tela que contém os processos necessários para o processamento do aplicativo referente ao estágio da leitura e analise do cartão
  //botão de voltar
  fill(255, 255, 255);
  background(255);

  pushMatrix();
  translate(width/2-100, height/2, 0);
  noFill();
  stroke(1);
  sphere(400);
  popMatrix();

  fill(256, 0, 0);
  rect(width-175, 40, 150, 30);
  fill(0, 0, 0);
  textAlign(CENTER);
  textSize(15);
  text("SAIR", width-100, 62);

  if (Serial.list().length ==1) {
    fill(0, 255, 0);
    rect(175, 40, 150, 30);
    fill(0, 0, 0);
    textAlign(CENTER);
    textSize(15);
    text("ENTRAR", 250, 62);
  } else {
    fill(256, 0, 0);
    rect(175, 40, 150, 30);
    fill(0, 0, 0);
    textAlign(CENTER);
    textSize(15);
    text("ENTRAR", 250, 62);
  }

  if (Serial.list().length ==1) {
    fill(0, 256, 0);
    rect(175+200, 40, 150, 30);
    fill(0, 0, 0);
    textAlign(CENTER);
    textSize(15);
    text("REINICIAR", 450, 62); //botão de voltar à tela anterior
  } else {
    fill(256, 0, 0);
    rect(175+200, 40, 150, 30);
    fill(0, 0, 0);
    textAlign(CENTER);
    textSize(15);
    text("REINICIAR", 450, 62); //botão de voltar à tela anterior
  }

  if (tela==1) {
    chamarOnline();
  } else if (tela==2) {
    onlineReading();
  }
}

void keyReleased() {
  if (tela==0) {
    if (key == 'e') {
      tela=1;
    }
  }
  if (tela==2) {
    if (key == 's') {
      log.close(); // Fecha o arquivo
      mySerial.clear();
      mySerial.stop();
      exit();
    }
  }
}

void mousePressed() {

  if (tela==0) {
    if (Serial.list().length ==1) {
      if (mouseX>175 && mouseX<(175+150) && mouseY>40 && mouseY<(40+30) ) {
        tela=1;
      }
    }
  }
  if (tela==2) {
    if (mouseX>375 && mouseX<(175+350) && mouseY>40 && mouseY<(40+30) ) {
      log.close(); // Fecha o arquivo
      mySerial.clear();
      mySerial.stop();
      delay(1000);
      tela=1;
    }
    if (mouseX>(width-175) && mouseX<(width-175+150) && mouseY>40 && mouseY<(40+30) ) {
      log.close(); // Fecha o arquivo
      mySerial.clear();
      mySerial.stop();
      exit();
    }
  } else if (tela==0) {
    if (mouseX>(width-175) && mouseX<(width-175+150) && mouseY>40 && mouseY<(40+30) ) {
      exit();
    }
  }
}
