# Kamus konversi kata-kata dari Inggris ke Indonesia
convert_word_to_indo = {
    "and" : "dan ",
    "not" : "engga ",
    "bro" : "cuy ",
    "sleepy": "mengontuuk ",
}

# Fungsi untuk mengonversi teks dari bahasa Inggris ke bahasa Indonesia
def convert_lang(text):
    res = ""
    
    # Cek jika teks adalah pesan default
    if(text == "Reload the page and try with another better image"):
        res = "Muat ulang halaman dan coba dengan gambar yang lebih baik."
    else:
        # Pisahkan kata-kata dalam teks
        wordArr = list(text.split(' '))
        res = "dia lagi "
        # Loop melalui setiap kata dan konversi ke bahasa Indonesia jika ada dalam kamus
        for word in wordArr:
            if(word in convert_word_to_indo):
                res += convert_word_to_indo[word]
        
    return res