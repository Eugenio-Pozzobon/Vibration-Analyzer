void chamarOnline() {//chama o cartão SD, inicializando a porta Serial

  if (Serial.list().length ==1) {//se houver alguma porta serial
    String portName = Serial.list()[0]; //configura a porta serial
    mySerial = new Serial(this, portName, 115200); //Configura a porta serial 2400000 maior velocidade porém carregando erros
    mySerial.write("o");
    tela=2;
  }
}

int numv=0;
float[] ax= new float[300];
float[] ay= new float[300];
float[] az= new float[300];
String[] Values=new String[10];
int c=0;

void onlineReading() {

  if (mousePressed) {
    camera(mouseX, mouseY, (height/2) / tan(PI/6), width/2, height/2, 0, 0, 1, 0);
  } else {
    camera(width/2, height/2, (height/2) / tan(PI/6), width/2, height/2, 0, 0, 1, 0);
  }

  for (int i=0; i<100; i++) {
    if (mySerial.available() > 0 ) { //Se receber um valor na porta serial
      String value = mySerial.readStringUntil('\n'); //Le o valor recebido até a quebra de linha do arquivo
      //se o valor recebido não for nulo, separa a linha com os dados entre virgulas, em dados separados.
      if (value != null) {
        linhaDados++; //incrementa o contador da quantidade de dado
        if (linhaDados>16) {
          log.print(value);
          print(value);
          Values = split(value, ',');
          if (Values.length==8) {
            pushMatrix();
            translate(width/2-100+map(float(Values[0]), -1.5, 1.5, -380, 380), height/2+map(float(Values[2]), -1.5, 1.5, -380, 380), +map(float(Values[1]), -1.5, 1.5, -380, 380));
            fill(255, 0, 0);
            sphere(20);
            popMatrix();
            stroke(0);
            pushMatrix();
            translate(width/2+400, height/2-250, 0);
            fill(255, 0, 0);
            line(0, -100, 0, 100);
             line(-10, 0, width-100, 0);
             fill(0);
             text("X AXIX", 0, 110);
            noFill();
            stroke(255, 0, 0);
            for (int v=1; v<c; v++) {
              line(v*10, map(ax[v-1], -1.5, 1.5, -100, 100), (v+1)*10, map(ax[v], -1.5, 1.5, -100, 100));
            }
            popMatrix();
            stroke(0);
            pushMatrix();
            translate(width/2+400, height/2, 0);
            fill(255, 0, 0);
            line(0, -100, 0, 100);
            line(-10, 0, width-100, 0);
                         fill(0);
             text("Y AXIX", 0, 110);
            noFill();
            stroke(0, 255, 0);
            beginShape();
            for (int v=1; v<c; v++) {
              line(v*10, map(ay[v-1], -1.5, 1.5, -100, 100), (v+1)*10, map(ay[v], -1.5, 1.5, -100, 100));
            }
            endShape();
            popMatrix();
            stroke(0);
            pushMatrix();
            translate(width/2+400, height/2+250, 0);
            fill(255, 0, 0);
            line(0, -100, 0, 100);
            line(-10, 0, width-100, 0); 
                         fill(0);
             text("Z AXIX", 0, 110);
            noFill();
            stroke(0, 0, 255);
            beginShape();
            for (int v=1; v<c; v++) {
              line(v*10, map(az[v-1], -1.5, 1.5, -100, 100), (v+1)*10, map(az[v], -1.5, 1.5, -100, 100));
            }
            endShape();
            popMatrix();
            stroke(0);
            for (int v=0; v<59; v++) {
              ax[v]=ax[v+1];
              ay[v]=ay[v+1];
              az[v]=az[v+1];
            }

            ax[59]=float(Values[0]);
            ay[59]=float(Values[1]);
            az[59]=float(Values[2]);

            c++;
            if (c>58) {
              c=0;
            }
            numv++;
            println(numv);
          }
        }
      }
    } else {
      mySerial.write("o");
    }
  }
} 
