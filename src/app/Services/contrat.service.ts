import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {Contrat} from "../Modals/Contrat";

@Injectable({
  providedIn: 'root'
})
export class ContratService {

  url : string = 'http://localhost:5000';
  constructor(private http: HttpClient) { }



  getprime(taille:number, age:number, term:number, nb_paiment:number, amount:number, i:number,differed:number){
    return this.http.get(`${this.url}/predict/${taille}/${age}/${term}/${nb_paiment}/${amount}/${i}/${differed}`)
  }


}
