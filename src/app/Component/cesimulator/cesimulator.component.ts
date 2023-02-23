import {Component, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {CEServiceService} from "../../Services/ceservice.service";
import {Options} from "@angular-slider/ngx-slider";
import {CanvasJS} from "../../../assets/canvasjs.angular.component";
import { ViewChild } from '@angular/core'
import {WebSocketServiceService} from "../../Services/web-socket-service.service";
import {ContratService} from "../../Services/contrat.service";
import {Contrat} from "../../Modals/Contrat";
import {FormGroup} from "@angular/forms";
@Component({
  selector: 'app-cesimulator',
  templateUrl: './cesimulator.component.html',
  styleUrls: ['./cesimulator.component.scss']
})
export class CESimulatorComponent implements OnInit,OnChanges {
  u:Object
  p:Object
  contrat=new Contrat();
  w:any;
  test: string ;
  testamount: any;
  testage: any;
  testprime:any;
  testn: any;
  testi: any;
  vie: number;
  diff:string;



  constructor(private service:ContratService) {

  }

  ngOnInit(): void {

  }
  ngOnChanges(changes: SimpleChanges):void{

  }

  simulate() {


    this.u = null;
    this.p = null;
    this.test = null;
    this.testage = null;
    this.testamount = null;
    this.testprime = null;
    this.diff=null;


    if((this.contrat.m>this.contrat.n) || (this.contrat.age>120) || (this.contrat.amount<=100) || (this.contrat.age+this.contrat.n>120)  ) {
      if ((this.contrat.m > this.contrat.n)) {
        this.test = 'verifiez le nombre de payements'
      }
      if ((this.contrat.age > 120)) {
        this.testage = "Age maximum 120"
      }
      if ((this.contrat.amount <= 0)) {
        this.testamount = "Montant doit etre positif"
      }
      if ((this.contrat.age + this.contrat.n > 120)) {
        this.testage = "Age maximum et durée depassent l'age maximal 120"
      }
    }
    else {
      this.service.getprime(this.contrat.taille, this.contrat.age, this.contrat.n, this.contrat.m, this.contrat.amount,
        this.contrat.i,this.contrat.differed).subscribe(res => {
        console.log(res);
        this.u = res[0]+ "€";
        this.p= res[1]+ "€";
        // @ts-ignore
        let x = Math.abs(res[0] - res[1])
        this.diff=x.toFixed(2)
      });

    }



  }
  clean() {
    this.contrat.n=null;
    this.contrat.m=null;
    this.contrat.amount=null;
    this.contrat.age=null;
    this.contrat.i=null;
    this.contrat.differed=null;
    this.contrat.taille=null;
    this.diff=null;
    this.u=null;
    this.p=null;
    this.test=null;
    this.testage=null;
    this.testamount=null;


  }
}
