#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Write out roots in there lowest form for Sym Express 3

    Copyright (C) 2024 Gien van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.



"""

from symexpress3          import symexpress3
from symexpress3.optimize import optimizeBase
from symexpress3          import primefactor  as primefac

class OptimizeOnlyOneRoot( optimizeBase.OptimizeBase ):
  """
  Write out roots in there lowest form
  \n 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)
  """
  def __init__( self ):
    super().__init__()
    self._name         = "onlyOneRoot"
    self._symtype      = "all"
    self._desc         = "Write out roots in there lowest form"


  def optimize( self, symExpr, action ):
    result = False
    if self.checkExpression( symExpr, action ) != True:
      # print( "Afgekeurd: " + symExpr.symType )
      return result

    # 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)

    # print( "_writeOutOnlyOneRoot start" )

    # simplify the factCounter
    # 27^^(1/2) = ((3^2)*3)^^(1/2) = 3 * 3^^(1/2)
    # for iCnt in range( 0, len( symExpr.elements )):
    for iCnt, elem in enumerate( symExpr.elements ) :
      # elem = symExpr.elements[ iCnt ]

      if not isinstance( elem, symexpress3.SymNumber ):
        continue
      # print( "elem.onlyOneRoot: {} {}".format( elem.onlyOneRoot, elem ) )
      if elem.onlyOneRoot != 1:
        continue
      if elem.factSign != 1 :
        continue
      if elem.powerDenominator == 1 :
        continue
      if elem.factCounter == 1:
        if ( elem.powerSign == 1 and elem.powerCounter == 1 and elem.factDenominator == 1 ):
          elem.powerDenominator = 1
        continue

      # print( "OnlyOneRout: " + str( elem ))
      # symFact = SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
      # symDeno = SymExpress( '*', elem.powerSign, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)
      symFact = symexpress3.SymExpress( '*', 1, 1, 1, elem.onlyOneRoot )
      symDeno = symexpress3.SymExpress( '*', 1, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)

      lFoundOne = False
      dPrimeSet = primefac.factorint( elem.factCounter )
      for iPrime, iCount in dPrimeSet.items():
        # print( "iPrime: {}, iCount: {}, elem.powerDenominator: {}".format( iPrime, iCount,elem.powerDenominator ))
        if iCount >= elem.powerDenominator :
          iFact = iCount // elem.powerDenominator
          iRad  = iCount % elem.powerDenominator
          lFoundOne = True

          elem1 = symexpress3.SymNumber( 1, int( iPrime ), 1, 1, iFact, 1, 1 )
          symFact.add ( elem1 )

          if iRad > 0 :
            elem1 = symexpress3.SymNumber( 1, int( iPrime ), 1, 1, iRad, 1, 1 )
            symDeno.add ( elem1 )
        else:
          elem1 = symexpress3.SymNumber( 1, int( iPrime ), 1, 1, iCount, 1, 1 )
          symDeno.add ( elem1 )

      if lFoundOne == True:
        result = True
        # print( "symExpr   : {}".format( str( symExpr)))
        # print( "Fact   : {}".format( str( symFact )))
        # print( "symDeno: {}".format( str( symDeno )))

        if elem.factDenominator > 1 :
          elem1 = symexpress3.SymNumber( 1, 1, elem.factDenominator, 1, 1, 1 )
          symDeno.add( elem1 )

        symReplace = symexpress3.SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
        symReplace.add( symFact )
        if symDeno.numElements() > 0:
          symReplace.add( symDeno )

        # print( "fact old elem: {}".format( str( elem )))
        # print( "fact new elem: {}".format( str( symReplace)))

        symExpr.elements[ iCnt ] = symReplace

    # simplify the factDenominator
    # (1/27)^^(1/2) = (((1/3)^2)*3)^^(1/2) = 1/3 * 3^^(1/2)
    # for iCnt in range( 0, len( symExpr.elements )):
    for iCnt, elem in enumerate( symExpr.elements ):
      # elem = symExpr.elements[ iCnt ]

      # print( "check: {}".format( str( elem )))

      if not isinstance( elem, symexpress3.SymNumber ):
        continue
      if elem.onlyOneRoot != 1 :
        continue
      if elem.factSign != 1 :
        continue
      if elem.powerDenominator == 1 :
        continue
      if elem.factDenominator == 1 :
        continue

      # print( "check 2: deno:{}, elem: {}".format( elem.factDenominator, str( elem )))

      # symFact = SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
      # symDeno = SymExpress( '*', elem.powerSign, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)
      symFact = symexpress3.SymExpress( '*', 1, 1, 1, elem.onlyOneRoot )
      symDeno = symexpress3.SymExpress( '*', 1, elem.powerCounter, elem.powerDenominator, elem.onlyOneRoot)

      lFoundOne = False
      dPrimeSet = primefac.factorint( elem.factDenominator )

      # print ( "dPrimeSet factDenominator: {}".format( dPrimeSet ))
      for iPrime, iCount in dPrimeSet.items():
        # print( "iPrime: {}, iCount: {}, elem.powerDenominator: {}".format( iPrime, iCount,elem.powerDenominator ))
        if iCount >= elem.powerDenominator :
          iDenom    = iCount // elem.powerDenominator
          iRad      = iCount % elem.powerDenominator
          lFoundOne = True

          elem1 = symexpress3.SymNumber( 1, 1, int( iPrime ), 1, iDenom, 1, 1 )
          symFact.add ( elem1 )

          if iRad > 0 :
            elem1 = symexpress3.SymNumber( 1, 1, int( iPrime ), 1, iRad, 1, 1 )
            symDeno.add ( elem1 )
        else:
          elem1 = symexpress3.SymNumber( 1, 1, int( iPrime ), 1, iCount, 1, 1 )
          symDeno.add ( elem1 )

      if lFoundOne == True :
        # print( "symExpr   : {}".format( str( symExpr)))
        # print( "Fact   : {}".format( str( symFact )))
        # print( "symDeno: {}".format( str( symDeno )))

        if elem.factCounter > 1 :
          elem1 = symexpress3.SymNumber( 1, elem.factCounter, 1, 1, 1, 1 )
          symDeno.add( elem1 )

        # symReplace = SymExpress( '*' )
        symReplace = symexpress3.SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )

        symReplace.add( symFact )
        if symDeno.numElements() > 0:
          symReplace.add( symDeno )

        # print( "deno old elem: {}".format( str( elem )))
        # print( "deno new elem: {}".format( str( symReplace)))
        symExpr.elements[ iCnt ] = symReplace

    # eliminate the factDenominator
    # (1/3)^(1/2) = 3 * 3^(1/2)

    # cBefore = str( symExpr )
    # dBefore = symExpr.getValue()
    # for iCnt in range( 0, len( symExpr.elements )):
    for iCnt, elem in enumerate( symExpr.elements ):
      # elem = symExpr.elements[ iCnt ]

      # print( "check: {}".format( str( elem )))

      if not isinstance( elem, symexpress3.SymNumber ):
        continue
      if elem.onlyOneRoot != 1 :
        continue
      if elem.factSign != 1 :
        continue
      if elem.powerDenominator == 1 :
        continue
      if elem.factDenominator == 1 :
        continue

      elemnew = elem.copy()
      elemnew.factDenominator = 1
      elemnew.powerSign       = 1
      elemfact = symexpress3.SymNumber( 1, 1, elem.factDenominator, 1, 1, 1 )

      iFactCounter = elem.factCounter
      # print( "iFactCounter: {}".format( iFactCounter ))
      for iFact in range( 1, elem.powerDenominator ):
        iFactCounter *= elem.factDenominator
        # print( "iFactCounter: {} = {}".format( iFact, iFactCounter ))
      elemnew.factCounter = iFactCounter

      symReplace = symexpress3.SymExpress( '*', elem.powerSign, 1, 1, elem.onlyOneRoot )
      symReplace.add( elemfact )
      symReplace.add( elemnew )

      #dValueElem = elem.getValue()
      #dValueRep  = symReplace.getValue()
      #if ( dValueElem != dValueRep ):
      #  print( "quotation old elem: {} = {}".format( dValueElem, str( elem )))
      #  print( "quotation new elem: {} = {}".format( dValueRep , str( symReplace)))

      symExpr.elements[ iCnt ] = symReplace
      result = True

    #cAfter = str( symExpr )
    #dAfter = symExpr.getValue()
    #if ( True or dAfter != dBefore ):
    #   print( "quotation before: {} = {}".format( dBefore, cBefore))
    #   print( "quotation after : {} = {}".format( dAfter , cAfter ))
    return result


#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """

  def _Check( testClass, symOrg, symTest, wanted ):
    if display == True :
      print( f"naam      : {testClass.name}" )
      print( f"orginal   : {str( symOrg  )}" )
      print( f"optimized : {str( symTest )}" )

    if str( symTest ).strip() != wanted:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'optimize {testClass.name}, unit test error: {str( symTest )}, value: {str( symOrg )}' )

  symTest = symexpress3.SymFormulaParser( '27^^(1/2)' )
  symTest.optimize()
  # symTest = symTest.elements[ 0 ]
  # symexpress3.SymExpressTree( symTest )
  symOrg = symTest.copy()

  testClass = OptimizeOnlyOneRoot()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "3 * (3)^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '(1/27)^^(1/2)' )
  symTest.optimize()
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "(1/3) * ((1/3))^^(1/2)" )


  symTest = symexpress3.SymFormulaParser( '(1/3)^^(1/2)' )
  symTest.optimize()
  symTest.optimize( "multiply" )
  symTest.optimize()
  symOrg = symTest.copy()
  testClass.optimize( symTest, "onlyOneRoot" )

  _Check( testClass, symOrg, symTest, "(1/3) * 3^^(1/2)" )


if __name__ == '__main__':
  Test( True )
