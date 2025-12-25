import { Component, OnInit } from '@angular/core';
import { NotesService } from '../../services/notes.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { Note } from '../../models/models';
import { marked } from 'marked';

@Component({
  selector: 'app-notes-list',
  templateUrl: './notes-list.component.html',
  styleUrls: ['./notes-list.component.css']
})
export class NotesListComponent implements OnInit {
  notes: Note[] = [];
  selectedNote: Note | null = null;
  isEditing = false;
  showEditor = false;
  searchQuery = '';
  
  editForm = {
    title: '',
    content: ''
  };

  constructor(
    private notesService: NotesService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadNotes();
  }

  loadNotes(): void {
    this.notesService.getNotes().subscribe({
      next: (response) => {
        this.notes = response.notes;
      },
      error: (error) => {
        console.error('Error loading notes:', error);
      }
    });
  }

  selectNote(note: Note): void {
    this.selectedNote = note;
    this.isEditing = false;
    this.showEditor = false;
  }

  createNewNote(): void {
    this.selectedNote = null;
    this.isEditing = true;
    this.showEditor = true;
    this.editForm = {
      title: '',
      content: ''
    };
  }

  editNote(): void {
    if (this.selectedNote) {
      this.isEditing = true;
      this.showEditor = true;
      this.editForm = {
        title: this.selectedNote.title,
        content: this.selectedNote.content
      };
    }
  }

  saveNote(): void {
    if (this.selectedNote) {
      // Update existing note
      this.notesService.updateNote(this.selectedNote.id, this.editForm).subscribe({
        next: () => {
          this.loadNotes();
          this.isEditing = false;
          this.showEditor = false;
        },
        error: (error) => {
          console.error('Error updating note:', error);
        }
      });
    } else {
      // Create new note
      this.notesService.createNote(this.editForm).subscribe({
        next: () => {
          this.loadNotes();
          this.isEditing = false;
          this.showEditor = false;
        },
        error: (error) => {
          console.error('Error creating note:', error);
        }
      });
    }
  }

  deleteNote(): void {
    if (this.selectedNote && confirm('Are you sure you want to delete this note?')) {
      this.notesService.deleteNote(this.selectedNote.id).subscribe({
        next: () => {
          this.selectedNote = null;
          this.loadNotes();
        },
        error: (error) => {
          console.error('Error deleting note:', error);
        }
      });
    }
  }

  cancelEdit(): void {
    this.isEditing = false;
    this.showEditor = false;
  }

  searchNotes(): void {
    if (this.searchQuery.trim()) {
      this.notesService.searchNotes(this.searchQuery).subscribe({
        next: (response) => {
          this.notes = response.notes;
        },
        error: (error) => {
          console.error('Error searching notes:', error);
        }
      });
    } else {
      this.loadNotes();
    }
  }

  renderMarkdown(content: string): string {
    return marked.parse(content) as string;
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: () => {
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.error('Error logging out:', error);
        this.router.navigate(['/login']);
      }
    });
  }
}
