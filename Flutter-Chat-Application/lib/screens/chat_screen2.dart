import 'package:flutter/material.dart';
import 'package:fluttericon/font_awesome_icons.dart';
import 'package:letschat/widgets/or_divider.dart';
import 'package:letschat/widgets/tabbutton_widget.dart';
import 'package:letschat/components/colors.dart';
import 'package:page_transition/page_transition.dart';
import 'login_screen.dart';
import 'chat_screen3.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:letschat/widgets/social_icons.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

final _firestore = FirebaseFirestore.instance;
User? loggedInuser;

class Continue extends StatefulWidget {
  static String id = 'continue';
  @override
  _ContinueState createState() => _ContinueState();
}

class _ContinueState extends State<Continue> {
  bool _obscureText = false;
  bool showSpinner = false;
  late String option;
  late String size;
  late String where;
  late String freq;
  final _text1 = TextEditingController();
  final _text2 = TextEditingController();
  final _text3 = TextEditingController();
  final _text4 = TextEditingController();

  bool _validate = false;
  final _auth = FirebaseAuth.instance;

  void getCurrentUser() {
    try {
      final user = _auth.currentUser;
      if (user != null) {
        loggedInuser = user;
        print(loggedInuser);
      }
    } catch (e) {
      print(e);
    }
  }

  void _toggle() {
    setState(() {
      _obscureText = !_obscureText;
    });
  }

  @override
  void dispose() {
    _text1.dispose();
    _text2.dispose();
    _text3.dispose();
    _text4.dispose();
    super.dispose();
  }

  @override
  void initState() {
    super.initState();
    getCurrentUser();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        image: DecorationImage(
          image: AssetImage('images/background.jpg'),
          fit: BoxFit.cover,
        ),
      ),
      constraints: BoxConstraints.expand(),
      child: Scaffold(
        resizeToAvoidBottomInset: false,
        backgroundColor: Colors.transparent,
        extendBodyBehindAppBar: true,
        appBar: AppBar(
          title: Text("Soon; magik..."),
          centerTitle: true,
          leading: IconButton(
            icon: Icon(Icons.arrow_back_ios_rounded),
            onPressed: () {
              Navigator.pop(context);
            },
          ),
          backgroundColor: Colors.transparent,
          elevation: 0.0,
        ),
        body: SafeArea(
          child: ListView(
            children: <Widget>[
              SizedBox(
                height: 20.0,
              ),
              /*
              Hero(
                tag: 'logo',
                child: Container(
                  height: 100.0,
                  child: Image.asset('images/logo.png'),
                ),
              ),*/
              SizedBox(
                height: 38.0,
              ),
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 30.0, vertical: 10.0),
                child: optionInput(),
              ),
              SizedBox(
                height: 5.0,
              ),
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 30.0, vertical: 10.0),
                child: sizeInput(),
              ),
              SizedBox(
                height: 5.0,
              ),
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 30.0, vertical: 10.0),
                child: whereInput(),
              ),
              SizedBox(
                height: 5.0,
              ),
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 30.0, vertical: 10.0),
                child: freqInput(),
              ),
              SizedBox(
                height: 5.0,
              ),
              Padding(
                padding: EdgeInsets.symmetric(horizontal: 30.0, vertical: 10.0),
                child: Hero(
                  tag: "button",
                  child: TabButton(
                    btnText: "Continue...",
                    btnTxtColor: Colors.white,
                    btnColor: PalletteColors.primaryRed,
                    btnFunction: () async {
                      (_text1.text.isEmpty ||
                              _text2.text.isEmpty ||
                              _text3.text.isEmpty ||
                              _text4.text.isEmpty)
                          ? _validate = true
                          : _validate = false;
                      setState(() {
                        showSpinner = true;
                      });
                      try {
                        _firestore.collection(loggedInuser!.uid).add({
                          "freq": freq,
                          "option": option,
                          "size": size,
                          "where": where,
                        });

                        Navigator.pushNamed(context, Final.id);
                        setState(() {
                          showSpinner = false;
                        });
                      } catch (e) {
                        print(e);
                      }
                    },
                  ),
                ),
              ),
              SizedBox(
                height: 5.0,
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    "Already have an account ?",
                    style: TextStyle(
                      fontSize: 15.0,
                      color: Colors.white,
                    ),
                  ),
                  TextButton(
                    onPressed: () {
                      Navigator.push(
                          context,
                          PageTransition(
                              type: PageTransitionType.fade,
                              child: LoginScreen()));
                    },
                    child: Text(
                      " Log In",
                      style: TextStyle(
                        fontSize: 15.0,
                        color: PalletteColors.primaryRed,
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(
                height: 14.0,
              ),
              OrDivider(),
              SizedBox(height: 20.0),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  SocialIcon(
                    colors: [
                      Color(0xFF102397),
                      Color(0xFF187adf),
                      Color(0xFF00eaf8),
                    ],
                    icon: Icon(FontAwesome.facebook, color: Colors.white),
                    onPressed: () {},
                  ),
                  SocialIcon(
                    colors: [
                      Color(0xFFff4f38),
                      Color(0xFFff355d),
                    ],
                    icon: Icon(FontAwesome.google, color: Colors.white),
                    onPressed: () {},
                  ),
                ],
              ),
              SizedBox(
                height: 30.0,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget optionInput() {
    return Theme(
      child: TextField(
        onChanged: (value) {
          option = value;
        },
        controller: _text2,
        style: TextStyle(
          color: Colors.white,
          fontSize: 16.0,
        ),
        keyboardType: TextInputType.name,
        decoration: InputDecoration(
          labelText: "Heating Oil or Propane?",
          // errorText: _validate ? 'Please Enter your name' : null,
          prefixIcon: Icon(Icons.question_answer_outlined),
          labelStyle: TextStyle(fontSize: 14, color: Colors.grey.shade400),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40),
            borderSide: BorderSide(
              color: Colors.grey.shade300,
            ),
          ),
          focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(40),
              borderSide: BorderSide(
                color: Colors.red,
              )),
          focusedErrorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40),
            borderSide: BorderSide(
              color: Colors.grey.shade300,
            ),
          ),
          errorStyle: TextStyle(fontSize: 14),
        ),
        textInputAction: TextInputAction.next,
      ),
      data: Theme.of(context).copyWith(
        accentColor: PalletteColors.primaryRed,
      ),
    );
  }

  Widget sizeInput() {
    return Theme(
      child: TextField(
        onChanged: (value) {
          size = value;
        },
        controller: _text1,
        style: TextStyle(
          color: Colors.white,
          fontSize: 16.0,
        ),
        keyboardType: TextInputType.number,
        decoration: InputDecoration(
          labelText: "Size of Tank in Litres",
          // errorText: _validate ? 'Please Enter your name' : null,
          prefixIcon: Icon(Icons.numbers_outlined),
          labelStyle: TextStyle(fontSize: 14, color: Colors.grey.shade400),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40),
            borderSide: BorderSide(
              color: Colors.grey.shade300,
            ),
          ),
          focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(40),
              borderSide: BorderSide(
                color: Colors.red,
              )),
          focusedErrorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40),
            borderSide: BorderSide(
              color: Colors.grey.shade300,
            ),
          ),
          errorStyle: TextStyle(fontSize: 14),
        ),
        textInputAction: TextInputAction.next,
      ),
      data: Theme.of(context).copyWith(
        accentColor: PalletteColors.primaryRed,
      ),
    );
  }

  Widget whereInput() {
    return Theme(
      child: TextField(
        onChanged: (value) {
          where = value;
        },
        controller: _text3,
        style: TextStyle(
          color: Colors.white,
          fontSize: 16.0,
        ),
        keyboardType: TextInputType.name,
        decoration: InputDecoration(
          labelText: "Whereabouts wrt house is the tank?",
          // errorText: _validate ? 'Please Enter your name' : null,
          prefixIcon: Icon(Icons.question_answer_outlined),
          labelStyle: TextStyle(fontSize: 14, color: Colors.grey.shade400),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40),
            borderSide: BorderSide(
              color: Colors.grey.shade300,
            ),
          ),
          focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(40),
              borderSide: BorderSide(
                color: Colors.red,
              )),
          focusedErrorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40),
            borderSide: BorderSide(
              color: Colors.grey.shade300,
            ),
          ),
          errorStyle: TextStyle(fontSize: 14),
        ),
        textInputAction: TextInputAction.next,
      ),
      data: Theme.of(context).copyWith(
        accentColor: PalletteColors.primaryRed,
      ),
    );
  }

  Widget freqInput() {
    return Theme(
      child: TextField(
        onChanged: (value) {
          freq = value;
        },
        controller: _text4,
        style: TextStyle(
          color: Colors.white,
          fontSize: 16.0,
        ),
        keyboardType: TextInputType.number,
        decoration: InputDecoration(
          labelText: "# times you would need a fill per year",
          // errorText: _validate ? 'Please Enter your name' : null,
          prefixIcon: Icon(Icons.numbers_outlined),
          labelStyle: TextStyle(fontSize: 14, color: Colors.grey.shade400),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40),
            borderSide: BorderSide(
              color: Colors.grey.shade300,
            ),
          ),
          focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(40),
              borderSide: BorderSide(
                color: Colors.red,
              )),
          focusedErrorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(40),
            borderSide: BorderSide(
              color: Colors.grey.shade300,
            ),
          ),
          errorStyle: TextStyle(fontSize: 14),
        ),
        textInputAction: TextInputAction.done,
      ),
      data: Theme.of(context).copyWith(
        accentColor: PalletteColors.primaryRed,
      ),
    );
  }
}
