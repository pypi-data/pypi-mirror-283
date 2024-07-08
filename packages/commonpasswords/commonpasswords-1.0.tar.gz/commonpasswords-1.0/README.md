# Common Password Dectetor
Hello this is a project that I've worked on because I'm bored! Anyway the purpose is to detect the security of an inputted password
checking for common patterns and common passwords.
## Warning
In default conditions I would reccomend only accepting 0 to -1 points
# Requirements
`Python 3.12` [Link](https://www.python.org/downloads/release/python-3120/)
# Quick Start
`1:` **Install the package:**
```
pip install git+https://github.com/TommyBoiss/Common-Password-Detector
```
`2.` **Import the library into your script:**
```
import commonpasswords
```
`3.` **Use the Detect function:**
```
import commonpasswords
commonpasswords.detect("[password]", True/False)
```
# Detect Function
The function "dectect" detects if the inputted password is common or unsecure
```
commonpasswords.detect(
Str, (Password: What password you are trying to detect), (Output > Int)
Bool, (Return Reasons: Returns reasons why points were deducted) (Output > Dict [points, [reasons]])
Dict, (Configuration: Allows you to configure the library more)
```

# Configure
*If data isn't entered here is will just resort to its default with no harm*
**IN YOUR DATABASE FILE ENSURE YOU HAVE NO BLANK LINES AT THE BOTTOM**
```
{
"startingpoints": Int,
"commonwordsdatabase" Str, # If you want to replace the default database input the path here

"commonlayout": {
  "enabled": bool, # (Enabled?)
  "pointsremove": Int, # (How many points to remove if the check fails)
  "pointsadd": Int, # (How many points to add if the check passes)
  "reason": Str, # (If the check fails what is the reason it failed)
  "minimin": Int # (Atleast how many characters much match the layout before failint)
},
"commonwords": {
  "enabled": bool, # (Enabled?)
  "pointsremove": Int, # (How many points to remove if the check fails)
  "pointsadd": Int, # (How many points to add if the check passes)
  "reason": Str, # (If the check fails what is the reason it failed)
},
"length": {
  "enabled": bool, # (Enabled?)
  "requirement": int # (How long does it have to be to pass)
  "pointsremove": Int, # (How many points to remove if the check fails)
  "pointsadd": Int, # (How many points to add if the check passes)
  "reason": Str, # (If the check fails what is the reason it failed)
},
"charactertypes": {
  "enabled": bool, # (Enabled?)
  "requirement": int # (How long does it have to be to pass)
  "pointsremove": Int, # (How many points to remove if the check fails)
  "pointsadd": Int, # (How many points to add if the check passes)
  "reason": Str, # (If the check fails what is the reason it failed)
},
"date": {
  "enabled": bool, # (Enabled?)
  "pointsremove": Int, # (How many points to remove if the check fails)
  "pointsadd": Int, # (How many points to add if the check passes)
  "reason": Str, # (If the check fails what is the reason it failed)
}

}
```

