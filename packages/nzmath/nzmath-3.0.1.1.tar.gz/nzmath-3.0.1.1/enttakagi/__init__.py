"""
====================================
Lectures on Elementary Number Theory
      (2nd Edition) by TAKAGI, Teiji
           notebook in Python-NZMATH(*1)
        Part 1 release on 2024/03/28
====================================

The purpose of this note is an easy introduction to Algorithmic Number
Theory --- ANT.  You can study three topics

    'Number Theory'
    'Python Programming'
    'English for Mathematics'(*2)

at a time, which are necessary for ANT, only by running and reading the
programs sec01.py, ..., sec60.py in this directory.  For that, you need
three preparations:

    Get the book by Takagi in the title above.(*3)
    Let Python & module NZMATH usable on your computer/smartphone.(*4)
    Download all files in this directory to your machine.

Then, on the command prompt or interactive shell, do

    $ python sec01.py

etc. and read the printed messages.(*5)  The programs themselves in the
files sec01.py, ... are easy English text to read.  That is all!(*6)

                        Tanaka, Satoru (TMCIT); NAKAMULA, Ken (TMU)(*7)
                                          2022/06/23 --- 2024/03/28

    (*1) Based on Python 3.8.16 and NZMATH 3.0.1.
    (*2) 'Japanese for Mathematics' to English readers.
    (*3) https://www.kyoritsu-pub.co.jp/book/b10011316.html
    (*4) https://www.python.org/ and https://nzmath.sourceforge.io/
    (*5) When running programs, you are requested to 'Hit Return!'
         so that you can continue after reading the printed messages.
    (*6) Finding and fixing bugs of Python calculator NZMATH on ANT is
         another important purpose for us developers.
    (*7) Special thanks to MATSUI, Tetsushi; OGURA, Naoki; MIYAMOTO,
         Yasunori and others on ACKNOWLEDGEMENTS.txt in the directory
         https://sourceforge.net/p/nzmath/code/ci/default/tree/dist/
         Home Page (NAKAMULA) https://tnt-nakamu-lab.fpark.tmu.ac.jp/

<<<< CONTENTS >>>>

Chapter 1   Elementary Number Theory
====================================
Section 1   Divisibility of Integers
------------------------------------
    sec01.py    Thm1_01, Thm1_02, Thm1_02_rem
Section 2   Greatest Common Divisors, Least Common Multiples
------------------------------------------------------------
    sec02.py    Thm1_03, Thm1_04, Thm1_05, Thm1_06, Prob1, Prob1_rem,
                Prob1_rem_eg, Prob2
Section 3   Linear Indeterminate Equations
------------------------------------------
    sec03.py    Thm1_07, Thm1_07_eg, Prob1, (Prob2 no idea)
Section 4   Primes
------------------
    sec04.py    Thm1_08, Thm1_09
    sec04a.py   Prob1, Prob2, Prob3, Prob4, PerfNumb, Prob5, LucasLehmer
    sec04b.py   Prob6, Prob7, gcdlcmFI, Prob8, Prob9, Prob10, Prob11
    sec04c.py   Prob12, Prob12_rem, Prob13, part_frac, Prob14, Prob14_rem
    sec04d.py   Thm1_10, PrimeTable, Thm1_10_rem, PrimeNumberTheorem,
                Tschebyschef, twinPrime, gapPrime, Goldbach

List of imported NZMATH functions & classes
===========================================
Suffixes to function names have the following meaning:
    '??' bug remain; '?-' bug fixed; '?=' minor change; '?+' newly added.
Those of no bug no change are no suffix.  Those applied again are omitted.
Arrow like A-->B implies imported function A quotes function B.
    utils.py    prod==arith1.product
    sec01.py    gcd.divmodl?+
    sec02.py    gcd.lcm?-, gcd.gcd?=, gcd.gcd_?+, gcd.modl?+, gcd.lcm_?+
    sec03.py    gcd.gcd_of_list?=, gcd.extgcd_?+, gcd.extgcd_gen?+
    sec04.py    factor.misc.primeDivisors?=-->factor.misc.FactoredInteger??,
                factor.methods.factor, prime.primonial
                factor.methods.trialDivision??-->factor.find.trialDivision??,
                factor.methods.rhomethod?=-->factor.find.rhomethod?=,
                factor.methods.pmom?=-->factor.find.pmom?=,
                factor.methods.mpqs??-->factor.mpqs.mpqsfind?-,
                factor.methods.ecm??-->factor.ecm.ecm??
    sec04a.py   factor.misc.countDivisors?+, multiplicative.sigma?=,
                factor.misc.sumDivisors?+, factor.misc.squarePart?=,
                factor.misc.allDivisors?=, prime.generator_eratosthenes,
                prime.primeq
    sec04b.py   combinatorial.combination_index_generator
    sec04c.py   combinatorial.binomial?-, combinatorial.multinomial,
                arith1.expand
    sec04d.py   arith1.floorsqrt, prime.generator, prime.nextPrime

List of utility functions in utils.py
=====================================
    HitRet, again, strInt, randFactLists
    lcm_def, allDivisors_def, gcd_def, countDivisors_def, sumDivisors_def

=========
Copyright
=========

The package is a part of NZMATH, and is distributed under the BSD
license.  See LICENSE.txt for detail.
"""
