rule detection_rule {
    meta:
        description = "Detects the specific challenge string"
        author = "picoCTF"
    strings:
        // Match the unique string in both ASCII and Unicode, ignoring case
         = "YaraRules0x100" ascii wide nocase
        
        // Match the Magic Header 'MZ' (4D 5A) at the start of the file
        // This ensures we don't accidentally flag text files (prevents False Positives)
         = "MZ"
    condition:
        ( at 0) and 
}
