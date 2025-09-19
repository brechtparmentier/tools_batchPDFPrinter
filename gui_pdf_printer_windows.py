#!/usr/bin/env python3
"""
GUI Smart Batch PDF Printer - Windows Versie

Grafische interface voor de batch PDF printer met drag & drop,
visuele preview en gebruiksvriendelijke bediening.
Aangepast voor Windows printer ondersteuning.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import subprocess
import threading
import logging
from pathlib import Path
from typing import List, Tuple
import time
import platform


class WindowsPDFPrinterGUI:
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
        self.root.title("🖨️ Smart Batch PDF Printer - Windows")
        self.root.geometry("1000x750")
        self.root.configure(bg='#f0f0f0')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🖨️ Smart Batch PDF Printer - Windows", 
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="🖨️ Printer Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        status_frame.columnconfigure(1, weight=1)
        
        self.printer_var = tk.StringVar(value="Bezig met controleren...")
        ttk.Label(status_frame, text="Standaard printer:").grid(row=0, column=0, sticky=tk.W)
        self.printer_label = ttk.Label(status_frame, textvariable=self.printer_var, 
                                      font=('Arial', 9, 'bold'))
        self.printer_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        self.refresh_printer_btn = ttk.Button(status_frame, text="🔄 Ververs", 
                                             command=self.check_printer_status)
        self.refresh_printer_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Directory selection frame
        dir_frame = ttk.LabelFrame(main_frame, text="📁 Map Selectie", padding="10")
        dir_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        dir_frame.columnconfigure(1, weight=1)
        
        ttk.Label(dir_frame, text="Geselecteerde map:").grid(row=0, column=0, sticky=tk.W)
        
        self.dir_var = tk.StringVar(value="Geen map geselecteerd")
        self.dir_label = ttk.Label(dir_frame, textvariable=self.dir_var, 
                                  relief='sunken', padding="5", background='white')
        self.dir_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        
        self.browse_btn = ttk.Button(dir_frame, text="📁 Bladeren", 
                                    command=self.browse_directory)
        self.browse_btn.grid(row=0, column=2)
        
        # Controls frame
        controls_frame = ttk.Frame(dir_frame)
        controls_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E))
        controls_frame.columnconfigure(1, weight=1)
        
        self.search_btn = ttk.Button(controls_frame, text="🔍 Zoek PDF's", 
                                    command=self.search_pdfs, state='disabled')
        self.search_btn.grid(row=0, column=0, sticky=tk.W)
        
        # Batch size setting
        ttk.Label(controls_frame, text="Batch grootte:").grid(row=0, column=1, sticky=tk.E, padx=(0, 5))
        
        self.batch_var = tk.StringVar(value="10")
        batch_spinbox = ttk.Spinbox(controls_frame, from_=1, to=50, width=5, 
                                   textvariable=self.batch_var)
        batch_spinbox.grid(row=0, column=2, sticky=tk.E)
        
        # PDF List frame
        list_frame = ttk.LabelFrame(main_frame, text="📄 Gevonden PDF Bestanden", padding="10")
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview voor PDF lijst
        self.tree = ttk.Treeview(list_frame, columns=('path', 'size'), show='tree headings')
        self.tree.heading('#0', text='Bestandsnaam')
        self.tree.heading('path', text='Locatie')
        self.tree.heading('size', text='Grootte')
        
        self.tree.column('#0', width=350)
        self.tree.column('path', width=450)
        self.tree.column('size', width=100)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scroll = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Action buttons frame
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))
        action_frame.columnconfigure(1, weight=1)
        
        self.print_btn = ttk.Button(action_frame, text="🖨️ Start Printen", 
                                   command=self.start_printing, state='disabled')
        self.print_btn.grid(row=0, column=0, sticky=tk.W)
        
        self.test_btn = ttk.Button(action_frame, text="🧪 Test Printer", 
                                  command=self.test_printer)
        self.test_btn.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        self.dry_run_btn = ttk.Button(action_frame, text="👁️ Preview (Dry Run)", 
                                     command=self.dry_run, state='disabled')
        self.dry_run_btn.grid(row=0, column=2, sticky=tk.E)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Voortgang", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Klaar om te beginnen")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="📋 Activiteiten Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 0))
        log_frame.columnconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Check printer status on startup
        self.root.after(500, self.check_printer_status)
        
    def log_message(self, message: str, level: str = "INFO"):
        """Log een bericht naar de GUI en log file."""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        
        # Log naar GUI
        self.log_text.insert(tk.END, log_entry + "\n")
        self.log_text.see(tk.END)
        
        # Log naar file
        if level == "ERROR":
            logging.error(message)
        elif level == "WARN":
            logging.warning(message)
        else:
            logging.info(message)
        
        # Update UI
        self.root.update_idletasks()
    
    def check_printer_status(self):
        """Controleer Windows printer status."""
        try:
            # Probeer standaard printer te vinden
            result = subprocess.run(['wmic', 'printer', 'where', 'default=true', 'get', 'name'], 
                                  capture_output=True, text=True, check=True, timeout=10)
            
            if result.stdout.strip() and 'No Instance(s) Available' not in result.stdout:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    printer_name = lines[-1].strip()
                    if printer_name and printer_name != 'Name':
                        self.printer_var.set(f"✅ {printer_name}")
                        self.log_message(f"Standaard printer gevonden: {printer_name}")
                        return
            
            self.printer_var.set("❌ Geen standaard printer")
            self.log_message("Geen standaard printer gevonden", "WARN")
            
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.printer_var.set("❓ Kan status niet controleren")
            self.log_message(f"Fout bij controleren printer: {e}", "ERROR")
    
    def browse_directory(self):
        """Open directory browser."""
        directory = filedialog.askdirectory(title="Selecteer map met PDF bestanden")
        if directory:
            self.dir_var.set(directory)
            self.search_btn.config(state='normal')
            self.log_message(f"Map geselecteerd: {directory}")
    
    def find_pdf_files(self, root_directory: str) -> List[Tuple[str, str, int]]:
        """Vind alle PDF bestanden recursief."""
        pdf_files = []
        
        try:
            for root, dirs, files in os.walk(root_directory):
                dirs.sort()  # Sorteer directories
                
                pdf_files_in_dir = [f for f in files if f.lower().endswith('.pdf')]
                pdf_files_in_dir.sort()
                
                for pdf_file in pdf_files_in_dir:
                    full_path = os.path.join(root, pdf_file)
                    try:
                        size = os.path.getsize(full_path)
                        pdf_files.append((full_path, root, size))
                    except OSError:
                        self.log_message(f"Kan bestandsgrootte niet bepalen: {full_path}", "WARN")
                        
        except Exception as e:
            self.log_message(f"Fout bij zoeken PDF's: {e}", "ERROR")
        
        # Sorteer: eerst op directory, dan op filename
        pdf_files.sort(key=lambda x: (x[1].lower(), os.path.basename(x[0]).lower()))
        return pdf_files
    
    def search_pdfs(self):
        """Zoek naar PDF bestanden in de geselecteerde directory."""
        directory = self.dir_var.get()
        if not directory or directory == "Geen map geselecteerd":
            messagebox.showerror("Fout", "Selecteer eerst een map")
            return
        
        if not os.path.exists(directory):
            messagebox.showerror("Fout", "Geselecteerde map bestaat niet")
            return
        
        self.log_message("Zoeken naar PDF bestanden...")
        self.progress_var.set("Zoeken naar PDF bestanden...")
        
        # Clear current list
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Find PDF files
        self.found_pdfs = self.find_pdf_files(directory)
        
        if not self.found_pdfs:
            self.log_message("Geen PDF bestanden gevonden", "WARN")
            self.progress_var.set("Geen PDF bestanden gevonden")
            messagebox.showinfo("Resultaat", "Geen PDF bestanden gevonden in de geselecteerde map")
            return
        
        # Populate tree
        for i, (full_path, directory_path, size) in enumerate(self.found_pdfs):
            filename = os.path.basename(full_path)
            size_str = self.format_file_size(size)
            rel_path = os.path.relpath(full_path, self.dir_var.get())
            
            self.tree.insert('', 'end', text=filename, values=(rel_path, size_str))
        
        self.log_message(f"{len(self.found_pdfs)} PDF bestanden gevonden")
        self.progress_var.set(f"{len(self.found_pdfs)} PDF bestanden gevonden")
        
        # Enable print buttons
        self.print_btn.config(state='normal')
        self.dry_run_btn.config(state='normal')
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def test_printer(self):
        """Test de printer met een voorbeeld bestand."""
        # Vraag gebruiker om een test PDF
        test_file = filedialog.askopenfilename(
            title="Selecteer een PDF om te testen",
            filetypes=[("PDF bestanden", "*.pdf"), ("Alle bestanden", "*.*")]
        )
        
        if not test_file:
            return
        
        try:
            self.log_message(f"Test printen: {os.path.basename(test_file)}")
            # Gebruik Windows standaard print actie
            os.startfile(test_file, "print")
            self.log_message("Test print opdracht verzonden naar printer")
            messagebox.showinfo("Test", "Test print opdracht verzonden!\nControleer of het document wordt afgedrukt.")
            
        except Exception as e:
            error_msg = f"Fout bij test printen: {e}"
            self.log_message(error_msg, "ERROR")
            messagebox.showerror("Fout", error_msg)
    
    def dry_run(self):
        """Toon wat er geprint zou worden zonder daadwerkelijk te printen."""
        if not self.found_pdfs:
            messagebox.showwarning("Waarschuwing", "Geen PDF bestanden gevonden")
            return
        
        try:
            batch_size = int(self.batch_var.get())
        except ValueError:
            batch_size = 10
        
        preview_window = tk.Toplevel(self.root)
        preview_window.title("👁️ Print Preview (Dry Run)")
        preview_window.geometry("600x500")
        
        frame = ttk.Frame(preview_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text=f"📋 Print Preview - {len(self.found_pdfs)} bestanden", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        ttk.Label(frame, text=f"Batch grootte: {batch_size} bestanden per batch").pack(pady=(0, 5))
        
        text_widget = scrolledtext.ScrolledText(frame, height=20, width=70)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Show files in print order
        for i, (full_path, _, size) in enumerate(self.found_pdfs, 1):
            batch_num = (i - 1) // batch_size + 1
            rel_path = os.path.relpath(full_path, self.dir_var.get())
            size_str = self.format_file_size(size)
            text_widget.insert(tk.END, f"{i:3d}. [Batch {batch_num}] {rel_path} ({size_str})\n")
        
        ttk.Button(frame, text="Sluiten", command=preview_window.destroy).pack(pady=(10, 0))
    
    def start_printing(self):
        """Start het print proces."""
        if not self.found_pdfs:
            messagebox.showwarning("Waarschuwing", "Geen PDF bestanden gevonden")
            return
        
        if self.is_printing:
            messagebox.showwarning("Waarschuwing", "Print proces is al bezig")
            return
        
        # Vraag bevestiging
        result = messagebox.askyesno(
            "Printen bevestigen", 
            f"Weet je zeker dat je {len(self.found_pdfs)} PDF bestanden wilt printen?\n\n"
            "Dit kan niet ongedaan worden gemaakt."
        )
        
        if not result:
            return
        
        try:
            self.batch_size = int(self.batch_var.get())
        except ValueError:
            self.batch_size = 10
        
        # Start printing in background thread
        self.is_printing = True
        self.print_btn.config(state='disabled')
        self.dry_run_btn.config(state='disabled')
        
        thread = threading.Thread(target=self.print_worker, daemon=True)
        thread.start()
    
    def print_worker(self):
        """Worker thread voor het print proces."""
        try:
            total_files = len(self.found_pdfs)
            printed_count = 0
            
            self.root.after(0, lambda: self.progress_bar.config(maximum=total_files))
            self.root.after(0, lambda: self.progress_var.set(f"Printen gestart - 0/{total_files}"))
            
            for i, (pdf_path, _, _) in enumerate(self.found_pdfs):
                if not self.is_printing:  # Check if cancelled
                    break
                
                try:
                    # Print using Windows
                    self.root.after(0, lambda p=pdf_path: self.log_message(f"Printen: {os.path.basename(p)}"))
                    
                    os.startfile(pdf_path, "print")
                    printed_count += 1
                    
                    self.root.after(0, lambda: self.progress_bar.config(value=printed_count))
                    self.root.after(0, lambda: self.progress_var.set(f"Geprint: {printed_count}/{total_files}"))
                    
                    # Wacht tussen bestanden om printer niet te overbelasten
                    if (i + 1) % self.batch_size == 0 and i + 1 < total_files:
                        self.root.after(0, lambda: self.log_message(f"Batch voltooid, wachten 3 seconden..."))
                        time.sleep(3)
                    else:
                        time.sleep(0.5)  # Korte pauze tussen bestanden
                    
                except Exception as e:
                    error_msg = f"Fout bij printen {os.path.basename(pdf_path)}: {e}"
                    self.root.after(0, lambda msg=error_msg: self.log_message(msg, "ERROR"))
            
            # Klaar
            if self.is_printing:
                self.root.after(0, lambda: self.log_message(f"Print proces voltooid! {printed_count}/{total_files} bestanden geprint"))
                self.root.after(0, lambda: messagebox.showinfo("Voltooid", f"Print proces voltooid!\n{printed_count}/{total_files} bestanden verzonden naar printer"))
            
        except Exception as e:
            error_msg = f"Onverwachte fout tijdens printen: {e}"
            self.root.after(0, lambda: self.log_message(error_msg, "ERROR"))
            self.root.after(0, lambda: messagebox.showerror("Fout", error_msg))
        
        finally:
            self.is_printing = False
            self.root.after(0, lambda: self.print_btn.config(state='normal'))
            self.root.after(0, lambda: self.dry_run_btn.config(state='normal'))
    
    def run(self):
        """Start de GUI applicatie."""
        self.log_message("Smart Batch PDF Printer gestart")
        self.log_message(f"Platform: {platform.platform()}")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.log_message("Applicatie afgesloten door gebruiker")


def main():
    """Hoofdfunctie."""
    if platform.system() != "Windows":
        print("❌ Deze versie is specifiek voor Windows")
        print("Gebruik de originele versie voor Linux/Mac")
        return
    
    try:
        app = WindowsPDFPrinterGUI()
        app.run()
    except Exception as e:
        print(f"❌ Fout bij starten applicatie: {e}")
        input("Druk Enter om af te sluiten...")


if __name__ == "__main__":
    main()
