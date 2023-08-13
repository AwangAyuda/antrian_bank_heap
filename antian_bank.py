import heapq
from gtts import gTTS
import os
import time
import pygame
import threading

class BankQueue:
    def __init__(self):
        self.queue1 = {"P": [], "B": []}
        self.queue2 = {"P": [], "B": []}
        self.current_ticket = {"K1P": 0, "K1B": 0, "K2P": 0, "K2B": 0}

    def get_ticket(self, kasir, tiket_type):
        self.current_ticket[f'{kasir}{tiket_type}'] += 1
        ticket = f'{kasir}{tiket_type}{str(self.current_ticket[f"{kasir}{tiket_type}"]).zfill(3)}'
        heapq.heappush(self.queue1[tiket_type], ticket)
        heapq.heappush(self.queue2[tiket_type], ticket)
        return ticket

    def next_customer(self, kasir, tiket_type):
        if kasir == "K1":
            queue = self.queue1
        else:
            queue = self.queue2

        if queue[tiket_type]:
            ticket = heapq.heappop(queue[tiket_type])
            self.speak(f'Antrian {kasir} nomor tiket {ticket} silahkan maju')

    def speak(self, text):
        def play_sound(output_file):
            pygame.mixer.init()
            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()

        output_file = f'output_{time.time()}.mp3'
        tts = gTTS(text=text, lang='id')
        tts.save(output_file)

        destination_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file)
        os.replace(output_file, destination_path)

        # Start playing sound in a separate thread
        sound_thread = threading.Thread(target=play_sound, args=(destination_path,))
        sound_thread.start()


def main():
    bank = BankQueue()
    while True:
        print("Selamat datang di Bank XYZ!")
        print("Pilih kasir:")
        print("1. Kasir 1")
        print("2. Kasir 2")
        print("0. Keluar")

        choice_kasir = input("Masukkan nomor kasir Anda: ")

        if choice_kasir == "1" or choice_kasir == "2":
            print("Pilih jenis tiket:")
            print("1. Pribadi")
            print("2. Bisnis")
            choice_tiket = input("Masukkan nomor jenis tiket Anda: ")

            if choice_tiket == "1":
                ticket = bank.get_ticket(f'K{choice_kasir}', 'P')
                print(f"Anda mendapatkan nomor antrian {ticket}. Mohon tunggu sekitar 5 detik sebelum dipanggil.")
                time.sleep(5)
                bank.next_customer(f'K{choice_kasir}', 'P')
            elif choice_tiket == "2":
                ticket = bank.get_ticket(f'K{choice_kasir}', 'B')
                print(f"Anda mendapatkan nomor antrian {ticket}. Mohon tunggu sekitar 5 detik sebelum dipanggil.")
                time.sleep(5)
                bank.next_customer(f'K{choice_kasir}', 'B')
            else:
                print("Pilihan tiket tidak valid. Silahkan masukkan pilihan yang benar.")
        elif choice_kasir == "0":
            print("Terima kasih telah menggunakan layanan kami. Sampai jumpa!")
            break
        else:
            print("Pilihan kasir tidak valid. Silahkan masukkan pilihan yang benar.")

if __name__ == "__main__":
    main()

