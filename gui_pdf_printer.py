#!/usr/bin/env python3
"""
GUI Smart Batch PDF Printer

Grafische interface voor de batch PDF printer met drag & drop,
visuele preview en gebruiksvriendelijke bediening.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import tkinter.dnd as dnd
import os
import sys
import subprocess
import threading
import logging
from pathlib import Path
from typing import List, Tuple
import time


class PDFPrinterGUI:
    def __init__(self):
        self.setup_logging()
        self.root = tk.Tk()
        self.setup_ui()
        self.found_pdfs = []
        self.batch_size = 10
        self.is_printing = False
        
    def setup_logging(self):
        """Setup logging configuratie."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('batch_pdf_printer.log'),
            ]
        )

    def setup_ui(self):
        """Setup de gebruikersinterface."""
        self.root.title("🖨️ Smart Batch PDF Printer")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🖨️ Smart Batch PDF Printer", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Directory selection frame
        dir_frame = ttk.LabelFrame(main_frame, text="📁 Map Selectie", padding="10")
        dir_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(1, weight=1)
        
        ttk.Label(dir_frame, text="Geselecteerde map:").grid(row=0, column=0, sticky=tk.W)
        
        self.dir_var = tk.StringVar(value="Geen map geselecteerd")
        self.dir_label = ttk.Label(dir_frame, textvariable=self.dir_var, 
                                  relief='sunken', padding="5")
        self.dir_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        self.browse_btn = ttk.Button(dir_frame, text="📁 Bladeren", 
                                    command=self.browse_directory)
        self.browse_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Search button
        self.search_btn = ttk.Button(dir_frame, text="🔍 Zoek PDF's", 
                                    command=self.search_pdfs, state='disabled')
        self.search_btn.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        # PDF List frame
        list_frame = ttk.LabelFrame(main_frame, text="📄 Gevonden PDF Bestanden", padding="10")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview voor PDF lijst
        self.tree = ttk.Treeview(list_frame, columns=('path', 'size'), show='tree headings')
        self.tree.heading('#0', text='Bestandsnaam')
        self.tree.heading('path', text='Locatie')
        self.tree.heading('size', text='Grootte')
        
        self.tree.column('#0', width=300)
        self.tree.column('path', width=400)
        self.tree.column('size', width=100)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Status label
        self.status_var = tk.StringVar(value="Selecteer een map om te beginnen")
        status_label = ttk.Label(list_frame, textvariable=self.status_var, 
                                font=('Arial', 9), foreground='blue')
        status_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Instellingen", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(settings_frame, text="Batch grootte:").grid(row=0, column=0, sticky=tk.W)
        
        self.batch_var = tk.StringVar(value="10")
        batch_spin = ttk.Spinbox(settings_frame, from_=1, to=50, width=5, 
                                textvariable=self.batch_var)
        batch_spin.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        ttk.Label(settings_frame, text="bestanden per batch").grid(row=0, column=2, 
                                                                   padx=(5, 0), sticky=tk.W)
        
        # Test button
        self.test_btn = ttk.Button(settings_frame, text="🧪 Test Printer", 
                                  command=self.test_printer)
        self.test_btn.grid(row=0, column=3, padx=(20, 0))
        
        # Action buttons frame
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        action_frame.columnconfigure(2, weight=1)
        
        self.preview_btn = ttk.Button(action_frame, text="👀 Preview", 
                                     command=self.show_preview, state='disabled')
        self.preview_btn.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))
        
        self.print_btn = ttk.Button(action_frame, text="🖨️ Print Alles", 
                                   command=self.start_printing, state='disabled')
        self.print_btn.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))
        
        self.stop_btn = ttk.Button(action_frame, text="⏹️ Stop", 
                                  command=self.stop_printing, state='disabled')
        self.stop_btn.grid(row=0, column=2, padx=(5, 0), sticky=(tk.W, tk.E))
        
        # Progress bar
        self.progress_var = tk.StringVar(value="")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var, 
                                  font=('Arial', 10, 'bold'))
        progress_label.grid(row=5, column=0, columnspan=3, pady=(0, 5))
        
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="📋 Log", padding="5")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Menu bar
        self.create_menu()
        
    def create_menu(self):
        """Maak menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bestand", menu=file_menu)
        file_menu.add_command(label="Map selecteren...", command=self.browse_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Afsluiten", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hulpmiddelen", menu=tools_menu)
        tools_menu.add_command(label="Test printer", command=self.test_printer)
        tools_menu.add_command(label="Log wissen", command=self.clear_log)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Over", command=self.show_about)

    def browse_directory(self):
        """Open directory browser."""
        directory = filedialog.askdirectory(title="Selecteer map met PDF bestanden")
        if directory:
            self.dir_var.set(directory)
            self.search_btn.config(state='normal')
            self.log_message(f"Map geselecteerd: {directory}")

    def search_pdfs(self):
        """Zoek PDF bestanden in geselecteerde directory."""
        directory = self.dir_var.get()
        if not directory or directory == "Geen map geselecteerd":
            messagebox.showwarning("Waarschuwing", "Selecteer eerst een map")
            return
            
        self.log_message("Zoeken naar PDF bestanden...")
        self.status_var.set("Zoeken...")
        self.search_btn.config(state='disabled')
        
        # Start search in separate thread
        thread = threading.Thread(target=self._search_thread, args=(directory,))
        thread.daemon = True
        thread.start()

    def _search_thread(self, directory):
        """Zoek PDF bestanden in separate thread."""
        try:
            pdf_files = []
            total_size = 0
            
            for root, dirs, files in os.walk(directory):
                dirs.sort()
                pdf_files_in_dir = [f for f in files if f.lower().endswith('.pdf')]
                pdf_files_in_dir.sort()
                
                for pdf_file in pdf_files_in_dir:
                    full_path = os.path.join(root, pdf_file)
                    try:
                        size = os.path.getsize(full_path)
                        total_size += size
                        pdf_files.append((root, pdf_file, size))
                    except OSError:
                        pass  # Skip files we can't access
            
            # Update UI in main thread
            self.root.after(0, self._update_pdf_list, pdf_files, total_size, directory)
            
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Fout bij zoeken: {e}"))
            self.root.after(0, lambda: self.search_btn.config(state='normal'))

    def _update_pdf_list(self, pdf_files, total_size, directory):
        """Update PDF lijst in UI."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Sort by directory then filename
        pdf_files.sort(key=lambda x: (x[0], x[1]))
        self.found_pdfs = [os.path.join(root, filename) for root, filename, _ in pdf_files]
        
        # Group by directory
        current_dir = None
        dir_item = None
        
        for root, filename, size in pdf_files:
            if root != current_dir:
                current_dir = root
                rel_dir = os.path.relpath(root, directory)
                if rel_dir == '.':
                    rel_dir = '📁 Hoofdmap'
                else:
                    rel_dir = f"📁 {rel_dir}"
                dir_item = self.tree.insert('', 'end', text=rel_dir, open=True)
            
            size_str = self.format_file_size(size)
            rel_path = os.path.relpath(os.path.join(root, filename), directory)
            
            self.tree.insert(dir_item, 'end', text=f"📄 {filename}", 
                           values=(rel_path, size_str))
        
        # Update status
        total_size_str = self.format_file_size(total_size)
        self.status_var.set(f"{len(pdf_files)} PDF bestanden gevonden ({total_size_str})")
        
        if pdf_files:
            self.preview_btn.config(state='normal')
            self.print_btn.config(state='normal')
        
        self.search_btn.config(state='normal')
        self.log_message(f"Zoeken voltooid: {len(pdf_files)} bestanden gevonden")

    def format_file_size(self, size_bytes):
        """Format file size in human readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"

    def show_preview(self):
        """Toon preview van wat afgedrukt zou worden."""
        if not self.found_pdfs:
            messagebox.showinfo("Info", "Geen PDF bestanden gevonden")
            return
            
        batch_size = int(self.batch_var.get())
        batches = [self.found_pdfs[i:i + batch_size] 
                  for i in range(0, len(self.found_pdfs), batch_size)]
        
        preview_text = f"PREVIEW - AFDRUKVOLGORDE\n\n"
        preview_text += f"Totaal: {len(self.found_pdfs)} bestanden in {len(batches)} batches\n"
        preview_text += f"Batch grootte: {batch_size} bestanden per batch\n\n"
        
        directory = self.dir_var.get()
        
        for batch_num, batch in enumerate(batches, 1):
            preview_text += f"=== BATCH {batch_num} ===\n"
            for pdf in batch:
                rel_path = os.path.relpath(pdf, directory)
                preview_text += f"  📄 {rel_path}\n"
            preview_text += "\n"
        
        # Show in new window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("👀 Afdruk Preview")
        preview_window.geometry("600x500")
        
        text_widget = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, preview_text)
        text_widget.config(state=tk.DISABLED)

    def test_printer(self):
        """Test de printer."""
        try:
            test_content = f"""
PDF PRINTER TEST

Dit is een test om te controleren of uw printer werkt.

Datum: {time.strftime("%Y-%m-%d %H:%M:%S")}
Systeem: {os.name}

Als u deze pagina kunt lezen, werkt uw printer correct.

Groeten,
Smart Batch PDF Printer
"""
            
            test_file = "/tmp/printer_test.txt"
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            result = subprocess.run(['lp', test_file], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_message("✅ Test pagina verzonden naar printer!")
                messagebox.showinfo("Success", "Test pagina verzonden naar printer!")
            else:
                error_msg = result.stderr or "Onbekende fout"
                self.log_message(f"❌ Fout bij printen: {error_msg}")
                messagebox.showerror("Fout", f"Printer test mislukt:\n{error_msg}")
            
            try:
                os.remove(test_file)
            except:
                pass
                
        except subprocess.TimeoutExpired:
            messagebox.showerror("Fout", "Printer test time-out. Controleer printer verbinding.")
        except FileNotFoundError:
            messagebox.showerror("Fout", "lp command niet gevonden. Installeer CUPS.")
        except Exception as e:
            self.log_message(f"Fout bij printer test: {e}")
            messagebox.showerror("Fout", f"Printer test fout: {e}")

    def start_printing(self):
        """Start het afdrukproces."""
        if not self.found_pdfs:
            messagebox.showwarning("Waarschuwing", "Geen PDF bestanden om af te drukken")
            return
        
        # Laatste bevestiging
        result = messagebox.askyesno(
            "Bevestiging", 
            f"Weet u zeker dat u {len(self.found_pdfs)} PDF bestanden wilt afdrukken?\n\n"
            "Dit kan niet ongedaan worden gemaakt."
        )
        
        if not result:
            return
        
        self.is_printing = True
        self.print_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress['maximum'] = len(self.found_pdfs)
        self.progress['value'] = 0
        
        # Start printing in separate thread
        thread = threading.Thread(target=self._print_thread)
        thread.daemon = True
        thread.start()

    def _print_thread(self):
        """Print PDF bestanden in separate thread."""
        batch_size = int(self.batch_var.get())
        batches = [self.found_pdfs[i:i + batch_size] 
                  for i in range(0, len(self.found_pdfs), batch_size)]
        
        successful = 0
        failed = 0
        current_file = 0
        
        for batch_num, batch in enumerate(batches, 1):
            if not self.is_printing:
                break
                
            self.root.after(0, lambda b=batch_num, t=len(batches): 
                          self.progress_var.set(f"Batch {b}/{t}"))
            
            for pdf_file in batch:
                if not self.is_printing:
                    break
                    
                current_file += 1
                rel_path = os.path.relpath(pdf_file, self.dir_var.get())
                
                self.root.after(0, lambda f=rel_path: 
                              self.log_message(f"Afdrukken: {f}"))
                
                try:
                    result = subprocess.run(['lp', pdf_file], 
                                          capture_output=True, text=True, 
                                          check=True, timeout=60)
                    successful += 1
                    self.root.after(0, lambda f=rel_path: 
                                  self.log_message(f"✅ Succesvol: {f}"))
                    logging.info(f"Successfully printed: {pdf_file}")
                    
                except subprocess.CalledProcessError as e:
                    failed += 1
                    error = e.stderr or "Onbekende fout"
                    self.root.after(0, lambda f=rel_path, err=error: 
                                  self.log_message(f"❌ Mislukt: {f} - {err}"))
                    logging.error(f"Failed to print {pdf_file}: {error}")
                
                except subprocess.TimeoutExpired:
                    failed += 1
                    self.root.after(0, lambda f=rel_path: 
                                  self.log_message(f"❌ Time-out: {f}"))
                
                self.root.after(0, lambda: self.progress.config(value=current_file))
            
            # Pause tussen batches
            if batch_num < len(batches) and self.is_printing:
                self.root.after(0, lambda: self.log_message("⏳ Wacht 3 seconden..."))
                time.sleep(3)
        
        # Finished
        self.root.after(0, self._print_finished, successful, failed)

    def _print_finished(self, successful, failed):
        """Called when printing is finished."""
        self.is_printing = False
        self.print_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
        if successful + failed > 0:
            self.progress_var.set(f"Voltooid: {successful} succesvol, {failed} mislukt")
            self.log_message(f"🏁 Afdrukken voltooid: {successful} succesvol, {failed} mislukt")
            
            if failed == 0:
                messagebox.showinfo("Voltooid", 
                                  f"Alle {successful} bestanden zijn succesvol afgedrukt!")
            else:
                messagebox.showwarning("Gedeeltelijk voltooid", 
                                     f"Afdrukken voltooid:\n"
                                     f"Succesvol: {successful}\n"
                                     f"Mislukt: {failed}")
        else:
            self.progress_var.set("Afgebroken")
            self.log_message("⏹️ Afdrukken geannuleerd")

    def stop_printing(self):
        """Stop het afdrukproces."""
        self.is_printing = False
        self.log_message("🛑 Stop gevraagd...")

    def log_message(self, message):
        """Voeg bericht toe aan log."""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def clear_log(self):
        """Wis log venster."""
        self.log_text.delete(1.0, tk.END)

    def show_about(self):
        """Toon over dialog."""
        about_text = """Smart Batch PDF Printer v1.0

Ontwikkeld voor het batch afdrukken van PDF bestanden
met gebruiksvriendelijke interface.

Functies:
• Recursief zoeken in mappen
• Alfabetische sortering
• Batch verwerking
• Visuele preview
• Real-time logging

Vereisten:
• Python 3.6+
• tkinter
• CUPS (Linux)

© 2024"""
        
        messagebox.showinfo("Over", about_text)

    def run(self):
        """Start de GUI applicatie."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    # Check if tkinter is available
    try:
        import tkinter
    except ImportError:
        print("❌ tkinter is niet beschikbaar. Installeer met:")
        print("   sudo apt-get install python3-tk")
        sys.exit(1)
    
    app = PDFPrinterGUI()
    app.run()