#include "core.hpp"
#include <cassert>
#include <cmath>
#include <stdexcept>
#include <limits>
int main(){using namespace lord_sumi;Counter c;c.add(10,5);c.add(10,5);auto w=c.result();assert(std::abs(w.rate-.5)<1e-12);assert(w.lower<.5&&w.upper>.5);bool bad=false;try{c.add(1,2);}catch(const std::invalid_argument&){bad=true;}assert(bad);bad=false;try{wilson(0,0);}catch(const std::invalid_argument&){bad=true;}assert(bad);bad=false;try{c.add(std::numeric_limits<std::uint64_t>::max(),0);}catch(const std::invalid_argument&){bad=true;}assert(bad);}