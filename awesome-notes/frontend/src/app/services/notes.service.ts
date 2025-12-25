import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Note } from '../models/models';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class NotesService {
  constructor(private http: HttpClient) {}

  getNotes(): Observable<{ notes: Note[] }> {
    return this.http.get<{ notes: Note[] }>(`${environment.apiUrl}/notes`);
  }

  getNote(id: number): Observable<{ note: Note }> {
    return this.http.get<{ note: Note }>(`${environment.apiUrl}/notes/${id}`);
  }

  createNote(note: { title: string; content: string }): Observable<{ message: string; note: Note }> {
    return this.http.post<{ message: string; note: Note }>(`${environment.apiUrl}/notes`, note);
  }

  updateNote(id: number, note: { title?: string; content?: string }): Observable<{ message: string; note: Note }> {
    return this.http.put<{ message: string; note: Note }>(`${environment.apiUrl}/notes/${id}`, note);
  }

  deleteNote(id: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${environment.apiUrl}/notes/${id}`);
  }

  searchNotes(query: string, from?: string, to?: string): Observable<{ notes: Note[]; count: number }> {
    let url = `${environment.apiUrl}/notes/search?q=${encodeURIComponent(query)}`;
    if (from) url += `&from=${from}`;
    if (to) url += `&to=${to}`;
    return this.http.get<{ notes: Note[]; count: number }>(url);
  }
}
