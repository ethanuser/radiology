"""Career stages (as of fall 2026) and the year each would typically start independent practice.

Assumes a 4-year MD/DO, PGY-1 + 4 diagnostic-radiology years, and a 1-year fellowship (most U.S. radiologists
complete one). Without a fellowship, subtract one year.
"""
STAGES = [
    ("premed", "Pre-med (college junior)", 2038),
    ("m1", "Medical student, year 1", 2036),
    ("m2", "Medical student, year 2", 2035),
    ("m3", "Medical student, year 3", 2034),
    ("m4", "Medical student, year 4", 2033),
    ("pgy1", "Intern (PGY-1)", 2032),
    ("r1", "Radiology resident, R1", 2031),
    ("r2", "Radiology resident, R2", 2030),
    ("r3", "Radiology resident, R3", 2029),
    ("r4", "Radiology resident, R4", 2028),
    ("fellow", "Fellow", 2027),
    ("attending", "Practicing radiologist", 2026),
]
