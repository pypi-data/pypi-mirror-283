import commonpasswords
def question():
    print(commonpasswords.detect(input("Password\n"), True, { "startingpoints": 10,
"commonlayout": {
  "enabled": True,
  "pointsremove": 5,
  "pointsadd": 2,
  "reason": "testing"
},
"commonwords": {
  "enabled": True,
  "pointsremove": 5,
  "pointsadd": 2,
  "reason": "test"
}

}))
    question()
question()
