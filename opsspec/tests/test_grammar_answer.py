from opsspec.specs import *

# considered explanation as answer
# answer => ops

spec_2jromeq5u9lloh1s = {
  "ops": [
    LagDiffOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
      field="Audience_Millions"
    )
  ],
  "ops2": [
    FindExtremumOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
      field="Audience_Millions",
      which="max"
    )
  ]
}

spec_13guplcbmfu1tjzu = {
  "ops": [
    FilterOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
      value=[]
    ),
  ],
  "ops2": [
    PairDiffOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
      field="Decrease_in_GDP_Percentage",
      by="Factor",
      groupA="Germany – exports",
      groupB="Italy – exports",
    )
  ],
}

spec_0q8vqyb35mbq0efx = {
  "ops":[
    FilterOp(
        id="n1",
        meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
        field="Age Group",
        include=["0–19 years"]
    ),
    SumOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
      field="Number of suicides"
    ),
    FilterOp(
        id="n3",
        meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
        field="Age Group",
        include=["20–39 years"]
    ),
    SumOp(
      id="n4",
      meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
      field="Number of suicides"
    ),
    FilterOp(
        id="n5",
        meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=1),
        field="Age Group",
        include=["40–64 years"]
    ),
    SumOp(
      id="n6",
      meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=1),
      field="Number of suicides"
    ),
    FilterOp(
        id="n7",
        meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=1),
        field="Age Group",
        include=["65 years and older"]
    ),
    SumOp(
      id="n8",
      meta=OpsMeta(nodeId="n8", inputs=["n7"], sentenceIndex=1),
      field="Number of suicides"
    ),
  ],

  "ops2": [
    FindExtremumOp(
      id="n9",
      meta=OpsMeta(nodeId="n9", inputs=["n2", "n4", "n6", "n8"], sentenceIndex=2),
      group="Year",
      field="Number of suicides",
      which="min"
    )
  ]
}

spec_2o3fyauxv32p571i={
  "ops":[
    SortOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
      order=["asc"],
      orderField="year",
      # group이 없어도 되는가?
    )
  ],
  "ops2": [
    FindExtremumOp(
        id="n2",
        meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
        field="Operating_Profit_Margin",
        which="min",
        rank=2
    )
  ]
}

spec_0s6zi9dyw22qo4rp={
  "ops":[
    FilterOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
      filed="Month/Year",
      value=["Sep 1896", "Oct 1896", "Nov 1896", "Dec 1896"]
    ),
    AverageOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
      field="Fatality rate among plague cases"
    )
  ],
  "ops2":[
    FilterOp(
      id="n3",
      meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
      filed="Month/Year",
      value=["Jan 1897", "Feb 1897", "Mar 1897", "Apr 1897", "May 1897"]
    ),
    AverageOp(
      id="n4",
      meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
      field="Fatality rate among plague cases"
    )
  ],
  "ops3":[
    DiffOp(
      id="n5",
      meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=2),
      field="Fatality rate among plague cases",
      targetA="ref:n2",
      targetB="ref:n4"
    )
  ]
}

# 방법 1
spec_2ebtadc07b7bo277={
  "ops":[
    SortOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
      field="Average price in US dollars",
      order=["asc"],
      orderField="Average price in US dollars"
    )
  ],
  "ops2":[
    FindExtremumOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
      field="Average price in US dollars",
      which=["min"],
      rank=2
    )
    
  ]
}

# 방법 2
"""
spec_2ebtadc07b7bo277={ 
  NthOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
      filed="Average price in US dollars",
      order=["asc"],
      orderField="",
      n:2
    )
  }
"""


spec_0rfuaawgi58ajpsv={
  "ops":[
    FilterOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
      field="Region",
      group="North America"
    ),
    AverageOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
      field="Media rights revenue in billion US dollars"
    )
  ],
  "ops2":[
    FilterOp(
      id="n3",
      meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
      field="Region",
      group="North America"
    ),
    AverageOp(
      id="n4",
      meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
      field="Media rights revenue in billion US dollars"
    )
  ],
  "ops3": [
    DiffOp(
      id="n3",
      meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
      field="Media rights revenue in billion US dollars",
      targetA="ref:n2",
      targetB="ref:n4"
    )
  ]
}

spec_0rdpculfpyw3bv5p={
  "ops":[
    DiffOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
      field="Value in billion US dollars",
      group="Type",
      by="Year",
      groupA="Lending",
      groupB="Investment"
    )
  ],
  "ops2":[
    FindExtremumOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
      group="Type",
      field="Value in billion US dollars",
      which=["min"],
      rank=1
    )
  ]
}

spec_10x2rgiqw97wdspi={
  "ops":[
    FilterOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
      field="Revenue_Million_Euros",
      group="Commercial"
    ),
    AverageOp(
      id="n2",
      meat=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
      field="Revenue_Million_Euros",
      group="Commercial"
    )
  ],

  "ops2":[
    FilterOp(
      id="n3",
      meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
      field="Revenue_Million_Euros",
      group="Broadcasting"
    ),
    AverageOp(
      id="n4",
      meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
      field="Revenue_Million_Euros",
      group="Broadcasting"
    )
  ],
  "ops3":[
    FilterOp(
      id="n5",
      meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
      field="Revenue_Million_Euros",
      operator=">",
      value=["ref:n2", "ref:n4"]
    )
  ]
}

'''ops2 재확인 필요'''
spec_0qz3v0bszsex7jjm={
  "ops":[
    AverageOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
      field="Expenditure in billion GBP",
      group="Fiscal Year"
    )
  ],
  "ops2":[
    CompareOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
      field="Expenditure in billion GBP",
      targetA="", # 전체 원 데이터를 어떻게 가져오지?
      targetB="ref:n1"
    )
  ],
  "ops3":[
    FilterOp(
      id="n3",
      meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
      field="Expenditure in billion GBP",
      value="ref:n1",
      operator="<"
    )
  ]
}

spec_28bxxhd6omv2l2h1={
  "ops":[
    PairDiffOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
      seriesField="Year",
      field="Life expectancy in years",
      groupA="Canada",
      groupB="Newfoundland and Labrador" 
    )
  ],
  "ops2":[
    FindExtremumOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=["n1"], senteceId=2),
      field="Life expectancy in years",
      which="max"
    )
  ]
}

spec_29rxoltwhongoday={
  "ops":[
    LagDiffOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=[], sentenceId=1),
      filed="Percentage",
    ),
    
  ],
  "ops2":[
    FilterOp(
      id="n2",
      meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceId=2),
      filed="Year",
      which="max"
    )
  ]
}

spec_2eiyyw562tcvjypp = {
  "ops": [
    FilterOp(
      id="n1",
      meta=OpsMeta(nodeId="n1", inputs=["n1"], sentenceId=1),
      field=""
    ),

  ],
  "ops2":[

  ]
}