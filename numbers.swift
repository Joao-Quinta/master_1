import SwiftKanren
import Foundation

public class Nat: ADT{
  public init(){
    super.init("Nat")

    self.add_generator("zero", Nat.zero)
    self.add_generator("succ", Nat.succ, arity: 1)

    self.add_operator("+", Nat.add, [
      Rule(
        Nat.add(Variable(named: "x"), Nat.zero()),
        Variable(named: "x")
      ),
      Rule(
        Nat.add(Variable(named: "x"), Nat.succ(Variable(named: "y"))),
        Nat.succ(Nat.add(Variable(named: "x"),Variable(named:"y"))))
    ],["nat", "nat"])
    
    // TODO: mul (multiplication)
    self.add_operator("*", Nat.mul,[
      Rule(Nat.mul(Variable(named: "x"), Nat.zero()), Nat.zero()), // x*0 = 0
      Rule(
              Nat.mul(Variable(named: "x"), Nat.succ(Variable(named: "y"))),
              Nat.add(Variable(named: "x"), Nat.mul(Variable(named: "x"), Variable(named: "y")))
      ) // x*(y+1) = x+(x*y)
    ],["nat", "nat"])
    
    // TODO: pre (predecessor) (pre(5) = 4)
    self.add_operator("pre", Nat.pre,[
      Rule(Nat.pre(Nat.succ(Variable(named: "x"))), Variable(named: "x")) // pre(x+1) = x
    ],["nat"])
    
    // TODO: sub (substraction)
    self.add_operator("-", Nat.sub,[
      Rule(Nat.sub(Variable(named: "x"), Nat.zero()), Variable(named: "x")), // x-0 = x
      Rule(
              Nat.sub(Variable(named: "x"), Nat.succ(Variable(named: "y"))),
              Nat.pre(Nat.sub(Variable(named: "x"), Variable(named: "y")))
      ) // x-(y+1) = (x-y)-1
    ],["nat", "nat"])
    
    // TODO: lt (lesser than) (4 < 3 -> False)
    self.add_operator("<", Nat.lt,[
      Rule(Nat.lt(Variable(named: "x"), Nat.zero()), Boolean.False()), // x<0 -> False (=> case x=0 False)
      Rule(Nat.lt(Nat.zero(), Variable(named: "x")), Boolean.True()), // 0<x -> True
      Rule(
              Nat.lt(Nat.succ(Variable(named: "x")), Nat.succ(Variable(named: "y"))),
              Nat.lt(Variable(named: "x"), Variable(named: "y"))
      ) // (x+1)<(y+1) -> x<y
    ],["nat", "nat"])
    
    // TODO: gt (greater than)
    self.add_operator(">", Nat.gt,[
      Rule(Nat.gt(Nat.zero(), Variable(named: "x")), Boolean.False()), // 0>x -> False (=> case x=0 False)
      Rule(Nat.gt(Variable(named: "x"), Nat.zero()), Boolean.True()), // x>0 -> True
      Rule(
              Nat.gt(Nat.succ(Variable(named: "x")), Nat.succ(Variable(named: "y"))),
              Nat.gt(Variable(named: "x"), Variable(named: "y"))
      ) // (x+1)>(y+1) -> x>y
    ],["nat", "nat"])
    
    // TODO: eq (equal)
    self.add_operator("==", Nat.eq,[
      Rule(
              Nat.eq(Variable(named: "x"), Variable(named: "y")),
              Boolean.not(Boolean.or(Nat.lt(Variable(named: "x"), Variable(named: "y")), Nat.gt(Variable(named: "x"), Variable(named: "y"))))
      ) // x==y -> !((x<y) or (x>y))
    ],["nat", "nat"])
    
    // TODO: mod (modulo) (10 % 4 = 2)
    // You can return vFail if it's undefined
    self.add_operator("%", Nat.mod,[
      Rule(Nat.mod(Variable(named: "x"), Nat.zero()), vFail), // div by 0 not defined
      Rule(Nat.mod(Variable(named: "x"), Variable(named: "y")), Nat.zero(), Nat.eq(Variable(named: "x"), Variable(named: "y"))), // case x=y : x%y = 0
      Rule(Nat.mod(Variable(named: "x"), Variable(named: "y")), Variable(named: x), Nat.lt(Variable(named: "x"), Variable(named: "y"))), // case x<y : x%y = x
      Rule(
              Nat.mod(Variable(named: "x"), Variable(named: "y")),
              Nat.mod(Nat.sub(Variable(named: "x"), Variable(named: "y")), Variable(named: "y")),
              Nat.gt(Variable(named: "x"), Variable(named: "y"))
      ) // case x>y : x%y = (x-y)%y
    ],["nat", "nat"])
    
    // TODO: gcd (Greatest common divisor) (gcd(20, 12) = 4)
    self.add_operator("gcd", Nat.gcd,[
      Rule(Nat.gcd(Variable(named: "x"), Nat.zero()), Variable(named: "x")), // gcd(x,0) = x
      Rule(Nat.gcd(Nat.zero(), Variable(named: "x")), Variable(named: "x")), // gcd(o,x) = x
      Rule(
              Nat.gcd(Variable(named: "x"), Variable(named: "y")),
              Variable(named: "y"),
              Nat.eq(Nat.mod(Variable(named: "x"), Variable(named: "y")), Nat.zero())
      ), // case x%y=0 : gcd(x,y) = y
      Rule(
              Nat.gcd(Variable(named: "x"), Variable(named: "y")),
              Nat.gcd(Variable(named: "y"), Nat.mod(Variable(named: "x"), Variable(named: "y"))),
              Nat.gt(Nat.mod(Variable(named: "x"), Variable(named: "y")), Nat.zero())
      ) // case x%y>0 : gcd(x,y) = gcd(y, x%y)
    ],["nat", "nat"])
    
    // TODO: div (euclidean division) (div(10/3) = 3)
    // You can return vFail if it's undefined
    self.add_operator("/", Nat.div,[
      Rule(Nat.div(Variable(named: "x"), Nat.zero()), vFail), // div by 0 not defined
      Rule(
              Nat.div(Variable(named: "x"), Variable(named: "y")),
              Nat.zero(),
              Boolean.or(Nat.lt(Variable(named: "x"), Variable(named: "y")), Nat.eq(Variable(named: "x"), Variable(named: "y")))
      ), // case x<=y : x/y = 0
      Rule(
              Nat.div(Variable(named: "x"), Variable(named: "y")),
              Nat.succ(Nat.div(Nat.sub(Variable(named: "x"), Variable(named: "y")), Variable(named: "y"))),
              Nat.gt(Variable(named: "x"), Variable(named: "y"))
      ) // case x>y : x/y = ((x-y)/y)+1
    ],["nat", "nat"])
  }

  //Generator
  static public func zero(_:Term...) -> Term{
    return new_term(Value<Int>(0),"nat")
  }

  static public func succ(_ x: Term...) -> Term {
    return new_term(Map(["succ": x[0]]),"nat")
  }

  static public func n(_ x: Int) -> Term {
  	if x==0{
  		return Nat.zero()
  	}
    var t = Nat.zero()
  	for _ in 1..<x+1 {
  		t = Nat.succ(t)
  	}
    return t
  }

  static public func to_int(_ term:Term) -> Int {
    if let map = (value(term) as? Map){
      if map["succ"] != nil{
        let k = Nat.to_int(map["succ"]!)
        return k+1
      }
    }
    return 0
  }

  public class override func belong(_ x: Term) -> Goal{
    return (x === Nat.zero() || delayed(fresh {y in x === Nat.succ(y) && Nat.belong(y)}))
  }

  public override func pprint(_ term: Term) -> String{
    return Nat.to_string(term)
  }


  static public func to_string(_ x: Term) -> String{
   	if x.equals(Nat.zero()){
   		return "0"
   	}
   	if let map = (value(x) as? Map){
      if map["succ"] != nil{
        let k = Nat.to_string(map["succ"]!)
        let f = k.components(separatedBy:"+")
        if f.count == 0{
          return k
        }
        if f.count == 1{
          if let i = Int(k){
            return String(1+i)
          }
          return "succ(\(k))"
        }
        if f[0].count == 0 {
     		   return "succ("+f[1]+")"
        }
        if let i = (Int(f[0])){
          return String(1+i)+" + "+f[1]
        }
        return "succ(\(k))"
      }
      return ADTm.pprint(map)
   	}
    if x is Variable {
      return "+"+ADTm.pprint(x)
    }
   	return ADTm.pprint(x)
  }

  public static func add(_ operands: Term...) -> Term{
      return Operator.n("+",operands[0], operands[1])
  }
  public static func mul(_ operands: Term...)-> Term{
    return Operator.n("*",operands[0], operands[1])
  }
  public static func pre(_ operands: Term...) -> Term{
    return Operator.n("pre", operands[0])
  }
  public static func sub(_ operands: Term...) -> Term{
    return Operator.n("-", operands[0], operands[1])
  }
  public static func div(_ operands: Term...) -> Term{
    return Operator.n("/", operands[0], operands[1])
  }
  public static func mod(_ operands: Term...) -> Term{
    return Operator.n("%", operands[0], operands[1])
  }
  public static func lt(_ operands: Term...) -> Term{
    return Operator.n("<", operands[0], operands[1])
  }
  public static func gt(_ operands: Term...) -> Term{
    return Operator.n(">", operands[0], operands[1])
  }
  public class func eq(_ operands: Term...) -> Term{
    return Operator.n("==", operands[0], operands[1])
  }
  public class func gcd(_ operands: Term...) -> Term{
    return Operator.n("gcd", operands[0], operands[1])
  }
}


public class Integer: ADT{
  public init(){
    super.init("int")
    self.add_generator("int", Integer.int)
    self.add_operator("+", Integer.add, [
      Rule(
        Integer.add(
          Integer.int(Variable(named: "a"),Variable(named: "b")),
          Integer.int(Variable(named: "c"),Variable(named: "d"))
        ),
        Integer.int(
          Nat.add(Variable(named: "a"),Variable(named: "c")),
          Nat.add(Variable(named: "b"),Variable(named: "d"))
        )
      )
    ], ["int", "int"])

 // TODO: sub (substraction)
    self.add_operator("-", Integer.sub, [
        Rule(
                Integer.sub(
                        Integer.int(Variable(named: "a"),Variable(named: "b")),
                        Integer.int(Variable(named: "c"),Variable(named: "d"))
                ),
                Integer.add(
                        InNatteger.int(Variable(named: "a"),Variable(named: "b")),
                        Integer.int(Variable(named: "d"),Variable(named: "c"))
                )
        ) // (a-b)-(c-d) = (a-b)+(d-c)
    ], ["int", "int"])

    // TODO: abs (absolute value) (abs(-3)) = 3
    // In the case of Integer: abs(0,3) = (3,0)
    self.add_operator("abs", Integer.abs, [
      Rule(Integer.abs(Integer.int(Variable(named: "x"), Nat.zero())), Integer.int(Variable(named: "x"), Nat.zero())), // abs(x-0) = x
      Rule(Integer.abs(Integer.int(Nat.zero(),Variable(named: "x"))), Integer.int(Variable(named: "x"), Nat.zero())), // abs(0-x) = x
      Rule(
              Integer.abs(Integer.int(Variable(named: "x"), Variable(named: "y"))),
              Integer.int(Nat.sub(Variable(named: "x"), Variable(named: "y")), Nat.zero()),
              Boolean.or(Nat.gt(Variable(named: "x"), Variable(named: "y")), Nat.eq(Variable(named: "x"), Variable(named: "y")))
      ), // case x>=y : abs(x-y) = ((x-y)-0)
      Rule(
              Integer.abs(Integer.int(Variable(named: "x"), Variable(named: "y"))),
              Integer.int(Nat.sub(Variable(named: "y"), Variable(named: "x")), Nat.zero()),
              Nat.lt(Variable(named: "x"), Variable(named: "y"))
      ) // case x<y : abs(x-y) = ((y-x)-0)
    ], ["int"])
    
    // TODO: normalize (normalize(4,2) = (2,0)
    // normalize(3,10) = (0,7))
    self.add_operator("normalize", Integer.normalize, [
        Rule(Integer.normalize(Integer.int(Variable(named: "x"), Nat.zero())), Integer.int(Variable(named: "x"), Nat.zero())), // norm(x-0) = (x-0)
        Rule(Integer.normalize(Integer.int(Nat.zero(),Variable(named: "x"))), Integer.int(Nat.zero(),Variable(named: "x"))), // norm(0-x) = (0-x)
        Rule(
                Integer.normalize(Integer.int(Variable(named: "x"), Variable(named: "y"))),
                Integer.int(Nat.sub(Variable(named: "x"), Variable(named: "y")), Nat.zero()),
                Boolean.or(Nat.gt(Variable(named: "x"), Variable(named: "y")), Nat.eq(Variable(named: "x"), Variable(named: "y")))
        ), // case x>=y : norm(x,y) = ((x-y)-0)
        Rule(
                Integer.normalize(Integer.int(Variable(named: "x"), Variable(named: "y"))),
                Integer.int(Nat.zero(), Nat.sub(Variable(named: "y"), Variable(named: "x"))),
                Nat.lt(Variable(named: "x"), Variable(named: "y"))
        ) // case x<y : norm(x,y) = (0-(y-x))
    ], ["int"])
    
    // TODO: mul (multiplication)
    self.add_operator("*", Integer.mul, [
      Rule(
              Integer.mul(Integer.int(Variable(named: "a"), Variable(named: "b")), Integer.int(Variable(named: "c"), Variable(named: "d"))),
              Integer.int(Nat.add(Nat.mul(Variable(named: "a"), Variable(named: "c")), Nat.mul(Variable(named: "b"), Variable(named: "a"))), Nat.add(Nat.mul(Variable(named: "a"), Variable(named: "d")), Nat.mul(Variable(named: "b"), Variable(named: "c"))))
      ) // (a-b)*(c-d) = (a*c+b*d)-(a*d+b*c)
    ], ["int", "int"])
    
    // TODO: eq (equal)
    self.add_operator("==", Integer.eq, [
      Rule(Integer.eq(Integer.int(Variable(named: "x"), Nat.zero()), Integer.int(Variable(named: "y"), Nat.zero())), Nat.eq(Variable(named: "x"), Variable(named: "y"))), // (x-0)==(y-0) -> x==y
      Rule(Integer.eq(Integer.int(Nat.zero(), Variable(named: "x")), Integer.int(Nat.zero(), Variable(named: "y"))), Nat.eq(Variable(named: "x"), Variable(named: "y"))), // (0-x)==(0-y) -> x==y
      Rule(Integer.eq(Integer.int(Nat.zero(), Variable(named: "x")), Integer.int(Variable(named: "y"), Nat.zero())), Boolean.False()), // (0-x)==(y-0) -> False
      Rule(Integer.eq(Integer.int(Variable(named: "x"), Nat.zero()), Integer.int(Nat.zero(), Variable(named: "y"))), Boolean.False()), // (x-0)==(0-y) -> False
      Rule(
              Integer.eq(Integer.int(Variable(named: "a"), Variable(named: "b")), Integer.int(Variable(named: "c"), Variable(named: "d"))),
              Integer.eq(Integer.normalize(Integer.int(Variable(named: "a"), Variable(named: "b"))), Integer.normalize(Integer.int(Variable(named: "c"), Variable(named: "d"))))
      ) // (a-b)==(c-d) -> norm(a-b)==norm(c-d)
    ], ["int", "int"])
    
    // TODO: lt (lesser than)
    self.add_operator("<", Integer.lt, [
      Rule(Integer.lt(Integer.int(Variable(named: "x"), Nat.zero()), Integer.int(Variable(named: "y"), Nat.zero())), Nat.lt(Variable(named: "x"), Variable(named: "y"))), // (x-0)<(y-0) -> x<y
      Rule(Integer.lt(Integer.int(Nat.zero(), Variable(named: "x")), Integer.int(Nat.zero(), Variable(named: "y"))), Nat.gt(Variable(named: "x"), Variable(named: "y"))), // (0-x)>(0-y) -> x>y
      Rule(Integer.lt(Integer.int(Variable(named: "x"), Nat.zero()), Integer.int(Nat.zero(), Variable(named: "y"))), Boolean.False()), // (x-0)<(0-y) -> False
      Rule(Integer.lt(Integer.int(Nat.zero(), Variable(named: "x")), Integer.int(Variable(named: "y"), Nat.zero())), Boolean.True()), // (0-x)<(y-0) -> True
      Rule(
              Integer.lt(Integer.int(Variable(named: "a"), Variable(named: "b")), Integer.int(Variable(named: "c"), Variable(named: "d"))),
              Integer.lt(Integer.normalize(Integer.int(Variable(named: "a"), Variable(named: "b"))), Integer.normalize(Integer.int(Variable(named: "c"), Variable(named: "d"))))
      ) // (a-b)<(c-d) -> norm(a-b)<norm(c-d)
    ], ["int", "int"])
    
    // TODO: gt (greater than)
    self.add_operator(">", Integer.gt, [
      Rule(Integer.gt(Integer.int(Variable(named: "x"), Nat.zero()), Integer.int(Variable(named: "y"), Nat.zero())), Nat.gt(Variable(named: "x"), Variable(named: "y"))), // (x-0)>(y-0) -> x>y
      Rule(Integer.gt(Integer.int(Nat.zero(), Variable(named: "x")), Integer.int(Nat.zero(), Variable(named: "y"))), Nat.lt(Variable(named: "x"), Variable(named: "y"))), // (0-x)>(0-y) -> x<y
      Rule(Integer.gt(Integer.int(Nat.zero(), Variable(named: "x")), Integer.int(Variable(named: "y"), Nat.zero())), Boolean.False()), // (0-x)>(y-0) -> False
      Rule(Integer.gt(Integer.int(Variable(named: "x"), Nat.zero()), Integer.int(Nat.zero(), Variable(named: "y"))), Boolean.True()), // (x-0)>(0-y) -> True
      Rule(
                Integer.gt(Integer.int(Variable(named: "a"), Variable(named: "b")), Integer.int(Variable(named: "c"), Variable(named: "d"))),
                Integer.gt(Integer.normalize(Integer.int(Variable(named: "a"), Variable(named: "b"))), Integer.normalize(Integer.int(Variable(named: "c"), Variable(named: "d"))))
      ) // (a-b)>(c-d) -> norm(a-b)>norm(c-d)
    ], ["int", "int"])
    
    // TODO: sign (sign(6,2) = True, sign(4,10) = False)
    // sign(0,0) = False
    self.add_operator("sign", Integer.sign, [
      Rule(
              Integer.sign(Integer.int(Variable(named: "x"), Variable(named: "y"))),
              Integer.gt(Integer.int(Variable(named: "x"), Variable(named: "y")), Integer.int(Nat.zero(), Nat.zero()))
      ) // sign(x-y) -> (x-y)>(0-0)
    ], ["int"])
    
    // TODO: div (euclidian division)
    // Help: Condition for the division is a simple xor which verify
    // a < b xor c < d (with integer1 = (a,b) and integer2 = (c,d)
    self.add_operator("/", Integer.div, [
      Rule(Integer.div(Integer.int(Variable(named: "x"), Variable(named: "y")), Integer.int(Nat.zero(), Nat.zero())), vFail), // div by 0 not defined
      Rule(
              Integer.div(Integer.int(Variable(named: "a"), Variable(named: "b")), Integer.int(Variable(named: "c"), Variable(named: "d"))),
              Integer.int(Nat.zero(), Nat.div(Nat.sub(Variable(named: "b"), Variable(named: "a")), Nat.sub(Variable(named: "c"), Variable(named: "d")))),
              Boolean.and(Nat.lt(Variable(named: "a"), Variable(named: "b")), Boolean.or(Nat.gt(Variable(named: "c"), Variable(named: "d")), Nat.eq(Variable(named: "c"), Variable(named: "d"))))
      ), // case a<b and c>=d : (a-b)/(c-d) = (0-((b-a)/(c-d)))
      Rule(
              Integer.div(Integer.int(Variable(named: "a"), Variable(named: "b")), Integer.int(Variable(named: "c"), Variable(named: "d"))),
              Integer.int(Nat.zero(), Nat.div(Nat.sub(Variable(named: "a"), Variable(named: "b")), Nat.sub(Variable(named: "d"), Variable(named: "c")))),
              Boolean.and(Nat.gt(Variable(named: "c"), Variable(named: "d")), Nat.lt(Variable(named: "a"), Variable(named: "b")))
      ), // case a>=b and c<d : (a-b)/(c-d) = (0-((a-b)/(d-c)))
      Rule(
              Integer.div(Integer.int(Variable(named: "a"), Variable(named: "b")), Integer.int(Variable(named: "c"), Variable(named: "d"))),
              Integer.int(Nat.div(Nat.sub(Variable(named: "a"), Variable(named: "b")), Nat.sub(Variable(named: "c"), Variable(named: "d"))), Nat.zero()),
              Boolean.and(Boolean.not(Nat.lt(Variable(named: "a"), Variable(named: "b"))), Boolean.not(Nat.lt(Variable(named: "c"), Variable(named: "d"))))
      ) // case a>=b and c>=d : (a-b)/(c-d) = (((a-b)/(c-d))-0)
    ], ["int", "int"])
  }

  static public func int(_ x: Term...) -> Term {
    return new_term(Map(["a": x[0], "b":x[1]]),"int")
  }

  static public func n(_ x: Int) -> Term {
    let abs_x = Swift.abs(x)
    if x>0{
      return Integer.int(Nat.n(abs_x),Nat.zero())
    }
    return Integer.int(Nat.zero(),Nat.n(abs_x))
  }

  static public func to_int(_ term:Term) -> Int {
    if let map = (value(term) as? Map){
      if map["a"] != nil && map["b"] != nil {
        let pos = Nat.to_int(map["a"]!)
        let neg = Nat.to_int(map["b"]!)
        return pos-neg
      }
    }
    return 0
  }

  public static func to_string(_ term: Term) -> String {
    if let map = (value(term) as? Map){
      if map["a"] != nil && map["b"] != nil {
        let pos = Nat.to_string(map["a"]!)
        let neg = Nat.to_string(map["b"]!)
        return "Int(+:\(pos), -:\(neg))"
      }
    }
    return ""
  }

  public class override func belong(_ x: Term) -> Goal{
    return (delayed(fresh {y in fresh {z in x === Integer.int(y,z) && Nat.belong(y) && Nat.belong(z)}}))
  }

  public override func pprint(_ term: Term) -> String{
    if let map = (value(term) as? Map) {

      let a : Term = ADTm.eval(map["a"]!)
      let b : Term = ADTm.eval(map["b"]!)
      if type(a)=="nat" && type(b) == "nat"{
        if ADTm.eval(Nat.eq(a,b)).equals(Boolean.True()){
          return "0"
        }
        if ADTm.eval(Nat.gt(a,b)).equals(Boolean.True()){
          return "+\(ADTm.pprint(ADTm.eval(Nat.sub(a,b))))"
        }
        return "-\(ADTm.pprint(ADTm.eval(Nat.sub(b,a))))"
      }
      return "FAIL"
    }
    if let variable = (term as? Variable){
      return variable.description
    }
    return Nat.to_string(term)
  }

  static public func add(_ terms: Term...)->Term{
    return Operator.n("+",terms[0], terms[1])
  }
  static public func sub(_ terms: Term...)->Term{
    return Operator.n("-",terms[0], terms[1])
  }
  static public func abs(_ terms: Term...)->Term{
    return Operator.n("abs",terms[0])
  }
  static public func normalize(_ terms: Term...)->Term{
    return Operator.n("normalize",terms[0])
  }
  static public func mul(_ terms: Term...)->Term{
    return Operator.n("*",terms[0], terms[1])
  }
  static public func eq(_ terms: Term...)->Term{
    return Operator.n("==",terms[0], terms[1])
  }
  public static func lt(_ operands: Term...) -> Term{
    return Operator.n("<", operands[0], operands[1])
  }
  public static func gt(_ operands: Term...) -> Term{
    return Operator.n(">", operands[0], operands[1])
  }
  public static func div(_ operands: Term...) -> Term{
    return Operator.n("/", operands[0], operands[1])
  }
  public static func sign(_ operands: Term...) -> Term{
    return Operator.n("sign", operands[0])
  }

}
