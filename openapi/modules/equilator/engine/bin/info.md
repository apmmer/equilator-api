Brief binary files description

Precompiled file ('precompiled.so') contains a stripped down version of equilator engine, it:
 - Calculates equity for each hand between 2 ranges.
 - Decrypts preflop matrix (enc_preflop_matrix.pkl)

Notes:
 - Multiprocessing (parallelization) is disabled.
 - Hand vs hand output is disabled. (Only hand vs range is enabled).
 - Opponents equity output is disabled.
 - Caching is disabled.
 - Using precalculated data (also caching) is disabled 
    (except'enc_preflop_matrix') to reduce weight of file.


file: enc_preflop_matrix.pkl contains an array with useless encrypted data.
    It should be decrypted by specific algorithm before usage.
