% Tambahkan basis pengetahuan gejala dan bobot
gejala(demam, 3).
gejala(batuk_kering, 3).
gejala(sesak_napas, 4).
gejala(kelelahan, 2).
gejala(kehilangan_penciuman_perasa, 4).
gejala(sakit_tenggorokan, 2).
gejala(sakit_kepala, 1).
gejala(nyeri_otot, 2).
gejala(hidung_tersumbat, 1).
gejala(mual_muntah, 1).
gejala(diare, 1).

% Tambahkan basis pengetahuan faktor risiko dan bobot
risiko(kontak_pasien, 5).
risiko(perjalanan_zona_merah, 4).

% Perbaikan diagnosis dengan penerapan bobot
diagnosis(Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Diagnosis, Rekomendasi) :-
    % Konversi jawaban ke nilai bobot
    bobot_gejala(Q1, demam, BobotQ1),
    bobot_gejala(Q2, batuk_kering, BobotQ2),
    bobot_gejala(Q3, sesak_napas, BobotQ3),
    bobot_gejala(Q4, kelelahan, BobotQ4),
    bobot_gejala(Q5, kehilangan_penciuman_perasa, BobotQ5),
    bobot_gejala(Q6, sakit_tenggorokan, BobotQ6),
    bobot_gejala(Q7, sakit_kepala, BobotQ7),
    bobot_gejala(Q8, nyeri_otot, BobotQ8),
    bobot_gejala(Q9, hidung_tersumbat, BobotQ9),
    bobot_gejala(Q10, mual_muntah, BobotQ10),
    bobot_gejala(Q11, diare, BobotQ11),
    
    % Bobot faktor risiko
    bobot_risiko(Q12, kontak_pasien, BobotQ12),
    bobot_risiko(Q13, perjalanan_zona_merah, BobotQ13),
    
    % Hitung total skor
    TotalBobot is BobotQ1 + BobotQ2 + BobotQ3 + BobotQ4 + BobotQ5 + BobotQ6 + BobotQ7 + BobotQ8 + BobotQ9 + BobotQ10 + BobotQ11,
    TotalRisiko is BobotQ12 + BobotQ13,
    
    % Tentukan keberadaan gejala khas (sesak napas dan kehilangan penciuman/perasa)
    deteksi_gejala_khas(Q3, Q5, GejalaKhasAda),
    
    % Tentukan diagnosis berdasarkan skor tertimbang
    diagnosis_level(TotalBobot, TotalRisiko, GejalaKhasAda, Diagnosis, Rekomendasi),
    
    % Format output untuk Python
    write('Diagnosis='), write(Diagnosis), write(','),
    write('Rekomendasi='), write(Rekomendasi), nl.

% Perhitungan bobot gejala
bobot_gejala('ya', Gejala, Bobot) :- gejala(Gejala, Bobot), !.
bobot_gejala(_, _, 0).

% Perhitungan bobot risiko
bobot_risiko('ya', Risiko, Bobot) :- risiko(Risiko, Bobot), !.
bobot_risiko(_, _, 0).

% Predicat untuk mendeteksi keberadaan gejala khas COVID-19
deteksi_gejala_khas(Q3, Q5, HasilDeteksi) :-
    (Q3 = 'ya', Q5 = 'ya') -> HasilDeteksi = 'ya' ;
    (Q3 = 'ya'; Q5 = 'ya') -> HasilDeteksi = 'mungkin' ;
    HasilDeteksi = 'tidak'.

% Aturan penentuan level diagnosis berdasarkan skor tertimbang dan kombinasi gejala
diagnosis_level(TotalBobot, TotalRisiko, GejalaKhasAda, Diagnosis, Rekomendasi) :-
    % Evaluasi berdasarkan kombinasi skor dan keberadaan gejala khas
    (
        % Kasus kecurigaan sangat tinggi - gejala khas + skor tinggi + faktor risiko tinggi
        (GejalaKhasAda = 'ya', TotalBobot >= 15, TotalRisiko >= 5) -> 
            Diagnosis = 'Tingkat Kecurigaan Sangat Tinggi COVID-19',
            Rekomendasi = 'Segera lakukan tes PCR dan isolasi mandiri. Hubungi hotline COVID-19 atau fasilitas kesehatan terdekat untuk penanganan segera.'
        ;
        % Kasus kecurigaan tinggi
        (TotalBobot >= 15, TotalRisiko >= 4) -> 
            Diagnosis = 'Tingkat Kecurigaan Tinggi COVID-19',
            Rekomendasi = 'Segera lakukan tes PCR dan isolasi mandiri. Hubungi fasilitas kesehatan terdekat untuk pemeriksaan lebih lanjut.'
        ;
        % Kasus kecurigaan sedang dengan gejala khas
        (GejalaKhasAda = 'ya', TotalBobot >= 8) -> 
            Diagnosis = 'Tingkat Kecurigaan Sedang COVID-19',
            Rekomendasi = 'Lakukan tes antigen/PCR. Lakukan isolasi mandiri sambil menunggu hasil tes. Pantau gejala dan saturasi oksigen secara berkala.'
        ;
        % Kasus kecurigaan sedang standar
        (TotalBobot >= 10, TotalRisiko >= 4) -> 
            Diagnosis = 'Tingkat Kecurigaan Sedang COVID-19',
            Rekomendasi = 'Lakukan tes antigen/PCR. Lakukan isolasi mandiri sambil menunggu hasil tes. Pantau gejala dan saturasi oksigen secara berkala.'
        ;
        % Kasus kecurigaan sedang karena faktor risiko tinggi
        (TotalBobot >= 5, TotalRisiko >= 5) ->
            Diagnosis = 'Tingkat Kecurigaan Sedang COVID-19 karena Faktor Risiko',
            Rekomendasi = 'Lakukan tes antigen. Batasi interaksi sosial hingga hasil tes keluar. Pantau gejala dengan cermat.'
        ;
        % Kasus kecurigaan rendah
        (TotalBobot >= 7) -> 
            Diagnosis = 'Tingkat Kecurigaan Rendah COVID-19',
            Rekomendasi = 'Lakukan tes antigen jika memungkinkan. Istirahat yang cukup dan pantau perkembangan gejala. Jika gejala memburuk, segera periksakan diri.'
        ;
        % Kasus gejala ringan
        (TotalBobot > 0) -> 
            Diagnosis = 'Gejala Ringan Tidak Spesifik COVID-19',
            Rekomendasi = 'Istirahat yang cukup, minum air putih, dan pantau gejala. Jika gejala menetap atau memburuk dalam 3 hari, pertimbangkan untuk tes COVID-19.'
        ;
        % Kasus tanpa gejala
        Diagnosis = 'Tidak Ada Gejala COVID-19 yang Signifikan',
        Rekomendasi = 'Tetap patuhi protokol kesehatan (memakai masker, mencuci tangan, menjaga jarak). Lakukan vaksinasi jika belum.'
    ).

% Menghitung jumlah jawaban 'ya' dalam list
count_ya([], 0).
count_ya(['ya'|T], N) :-
    count_ya(T, N1),
    N is N1 + 1.
count_ya([H|T], N) :-
    H \= 'ya',
    count_ya(T, N).

% Predikat untuk menampilkan hasil (digunakan oleh Python)
:- initialization(main).

main :-
    current_prolog_flag(argv, Argv),
    process_argv(Argv, Query),
    (Query \= [] -> 
        call_with_output(user_output, call(Query))
    ;
        true).

process_argv([], []).
process_argv(['-g', Query|_], Query) :- !.
process_argv([_|T], Query) :- process_argv(T, Query).

call_with_output(Stream, Goal) :-
    setup_call_cleanup(
        (set_prolog_IO(user_input, Stream, user_error),
            open_null_stream(Null)),
        (call(Goal), flush_output(Stream)),
        close(Null)).