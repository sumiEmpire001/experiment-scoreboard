#pragma once
#include <cmath>
#include <cstdint>
#include <limits>
#include <stdexcept>
namespace lord_sumi {
struct Wilson {double rate,lower,upper;};
inline Wilson wilson(std::uint64_t visitors,std::uint64_t conversions) {
 if(!visitors||conversions>visitors)throw std::invalid_argument("invalid counts");
 const double n=static_cast<double>(visitors),p=static_cast<double>(conversions)/n,z=1.96;
 const double d=1+z*z/n,center=(p+z*z/(2*n))/d;
 const double half=z*std::sqrt(p*(1-p)/n+z*z/(4*n*n))/d;
 return {p,std::fmax(0,center-half),std::fmin(1,center+half)};
}
struct Counter {std::uint64_t visitors=0,conversions=0;
 void add(std::uint64_t n,std::uint64_t k){
  if(!n||k>n||n>std::numeric_limits<std::uint64_t>::max()-visitors||k>std::numeric_limits<std::uint64_t>::max()-conversions)throw std::invalid_argument("invalid or overflowing counts");
  visitors+=n;conversions+=k;
 }
 Wilson result()const{return wilson(visitors,conversions);}
};
}