from opsspec.specs import *

spec_2jromeq5u9lloh1s = {
    "ops": [
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Audience_Millions"
        )
    ],
    "ops2":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Audience_Millions",
        )
    ],
    "ops3":[

    ]
}


spec_13guplcbmfu1tjzu = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Factor",
            include=["Germany – exports", "Italy – exports"]
        )
    ],
    "ops2":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Country",
            include=["Czechia"]
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Decrease_in_GDP_Percentage"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=2),
            field="Factor",
            include=["Hungary"]
        ),
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            field="Decrease_in_GDP_Percentage"
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1"], sentenceIndex=2),
            field="Factor",
            include=["Romania"]
        ),
        SumOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n6"], sentenceIndex=2),
            field="Decrease_in_GDP_Percentage"
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n1"], sentenceIndex=2),
            field="Factor",
            include=["Poland"]
        ),
        SumOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n1"], sentenceIndex=2),
            field="Decrease_in_GDP_Percentage"
        ),
    ],
    "ops3":[
        FindExtremumOp(
            id="n10",
            meta=OpsMeta(nodeId="n17", inputs=["n3", "n5", "n7", "n9"]),
            field="Decrease_in_GDP_Percentage",
            which="max"
        )
    ]
}


spec_0q8vqyb35mbq0efx = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2009"]
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Number of suicides"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2010"]
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Number of suicides"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2011"]
        ),
        SumOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=1),
            field="Number of suicides"
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2012"]
        ),
        SumOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n7"], sentenceIndex=1),
            field="Number of suicides"
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2013"]
        ),
        SumOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n9"], sentenceIndex=1),
            field="Number of suicides"
        ),
        FilterOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2014"]
        ),
        SumOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n11"], sentenceIndex=1),
            field="Number of suicides"
        ),
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2015"]
        ),
        SumOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n13"], sentenceIndex=1),
            field="Number of suicides"
        ),
        FilterOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2016"]
        ),
        SumOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=["n15"], sentenceIndex=1),
            field="Number of suicides"
        ),
        FilterOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2017"]
        ),
        SumOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=["n17"], sentenceIndex=1),
            field="Number of suicides"
        ),
        FilterOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2018"]
        ),
        SumOp(
            id="n20",
            meta=OpsMeta(nodeId="n20", inputs=["n19"], sentenceIndex=1),
            field="Number of suicides"
        ),
        FilterOp(
            id="n21",
            meta=OpsMeta(nodeId="n21", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2019"]
        ),
        SumOp(
            id="n22",
            meta=OpsMeta(nodeId="n22", inputs=["n21"], sentenceIndex=1),
            field="Number of suicides"
        ),
    ],
    "ops2":[
        FindExtremumOp(
            id="n23",
            meta=OpsMeta(nodeId="n23", inputs=["n2", "n4", "n6", "n8", "n10", "n12", "n14", "n16", "n18", "n20", "n22"], sentenceIndex=2),
            field="Number of suicides",
            which="min"
        )
    ],
    "ops3":[
        RetrieveValueOp(
            id="n24",
            meta=OpsMeta(nodeId="n24", inputs=["n23"], sentenceIndex=3),
            field="Year",
            target=2015
        )
    ]
}


spec_0o12tngadmjjux2n = {
    "ops":[
        AverageOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Production in million units"
        )
    ],
    "ops2":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Year",
            include=["1999"]
        ),
        CompareBoolOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n2",
            operator="<"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2000"]
        ),
        CompareBoolOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1", "n4"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n4",
            operator="<"
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2001"]
        ),
        CompareBoolOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n1", "n6"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n6",
            operator="<"
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2002"]
        ),
        CompareBoolOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n1", "n8"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n8",
            operator="<"
        ),
        FilterOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2003"]
        ),
        CompareBoolOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n1", "n10"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n10",
            operator="<"
        ),
        FilterOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2004"]
        ),
        CompareBoolOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=["n1", "n12"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n12",
            operator="<"
        ),
        FilterOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2005"]
        ),
        CompareBoolOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=["n1", "n15"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n15",
            operator="<"
        ),
        FilterOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2006"]
        ),
        CompareBoolOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=["n1", "n16"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n16",
            operator="<"
        ),
        FilterOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2007"]
        ),
        CompareBoolOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=["n1", "n18"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n18",
            operator="<"
        ),
        FilterOp(
            id="n20",
            meta=OpsMeta(nodeId="n20", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2008"]
        ),
        CompareBoolOp(
            id="n21",
            meta=OpsMeta(nodeId="n21", inputs=["n1", "n20"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n20",
            operator="<"
        ),
        FilterOp(
            id="n22",
            meta=OpsMeta(nodeId="n22", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2008"]
        ),
        CompareBoolOp(
            id="n23",
            meta=OpsMeta(nodeId="n23", inputs=["n1", "n22"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n22",
            operator="<"
        ),
        FilterOp(
            id="n24",
            meta=OpsMeta(nodeId="n24", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2008"]
        ),
        CompareBoolOp(
            id="n25",
            meta=OpsMeta(nodeId="n25", inputs=["n1", "n24"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n24",
            operator="<"
        ),
        FilterOp(
            id="n26",
            meta=OpsMeta(nodeId="n26", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2009"]
        ),
        CompareBoolOp(
            id="n27",
            meta=OpsMeta(nodeId="n27", inputs=["n1", "n26"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n26",
            operator="<"
        ),
        FilterOp(
            id="n28",
            meta=OpsMeta(nodeId="n28", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2010"]
        ),
        CompareBoolOp(
            id="n29",
            meta=OpsMeta(nodeId="n29", inputs=["n1", "n28"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n28",
            operator="<"
        ),
        FilterOp(
            id="n30",
            meta=OpsMeta(nodeId="n30", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2011"]
        ),
        CompareBoolOp(
            id="n31",
            meta=OpsMeta(nodeId="n31", inputs=["n1", "n30"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n30",
            operator="<"
        ),
        FilterOp(
            id="n32",
            meta=OpsMeta(nodeId="n32", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2012"]
        ),
        CompareBoolOp(
            id="n33",
            meta=OpsMeta(nodeId="n33", inputs=["n1", "n32"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n32",
            operator="<"
        ),
        FilterOp(
            id="n34",
            meta=OpsMeta(nodeId="n34", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2012"]
        ),
        CompareBoolOp(
            id="n35",
            meta=OpsMeta(nodeId="n35", inputs=["n1", "n34"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n34",
            operator="<"
        ),
        FilterOp(
            id="n36",
            meta=OpsMeta(nodeId="n36", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2013"]
        ),
        CompareBoolOp(
            id="n37",
            meta=OpsMeta(nodeId="n37", inputs=["n1", "n36"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n33",
            operator="<"
        ),
        FilterOp(
            id="n38",
            meta=OpsMeta(nodeId="n38", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2014"]
        ),
        CompareBoolOp(
            id="n39",
            meta=OpsMeta(nodeId="n39", inputs=["n1", "n38"], sentenceIndex=2),
            field="Production in million units",
            targetA="ref:n1",
            targetB="ref:n38",
            operator="<"
        )
    ],
    "ops3":[
        FilterOp(
            id="n39",
            meta=OpsMeta(nodeId="n39", inputs=[], sentenceIndex=3),
            operator="==",
            value=True
        ),
        CountOp(
            id="n40",
            meta=OpsMeta(nodeId="n40", inputs=["n3", "n5", "n7", "n9", "n11", "n13", "n15", "n17", "n19", "n21", "n23", "n25", "n27", "n29", "n32", "n35", "37", "39"], sentenceIndex=3)
        )
    ]
}


spec_10t8o5vhethzeod1 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Agriculture"
        ),
    ],
    "ops2":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Share_of_GDP",
            which="max"
        )
    ], 
    "ops3": [
        
    ]
}


spec_2o3fyauxv32p571i = {
    "ops":[
        
    ],
    "ops2":[
        SortOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=2),
            field="Operating_Profit_Margin",
            order="asc"
        ),
    ],
    "ops3":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=3),
            field="Operating_Profit_Margin",
            which="min"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
            field="Operating_Profit_Margin",
            which="min",
            rank=2
        )
    ],
    "ops4":[
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=4),
            field="Year",
            include=["2014", "2015"]
        )
    ]
}


spec_11e148qcs7x70t8v = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="South Korea"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            group="France"
        )
    ],
    "ops2":[
        CompareBoolOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Share_of_Import_Value",
            groupA="South Korea",
            groupB="France",
            operator=">"
        ),
    ],
}


spec_0s6zi9dyw22qo4rp ={
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Month/Year",
            include=["Sep 1896", "Oct 1896", "Nov 1896", "Dec 1896"]
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Fatality rate among plague cases"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Month/Year",
            include=["Jan 1897", "Feb 1897", "Mar 1897", "Apr 1897", "May 1897"]
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Fatality rate among plague cases"
        )
    ],
    "ops3":[
        CompareOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2","n4"], sentenceIndex=3),
            field="Fatality rate among plague cases",
            targetA="ref:n2",
            targetB="ref:n4",
            which="max"
        )
    ]
}


spec_2ebtadc07b7bo277 = {
    "ops":[
        
    ],
    "ops2":[
        SortOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=2),
            field="Average price in US dollars",
            order="asc"
        )
    ],
    "ops3":[
        RetrieveValueOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=3),
            field="Year",
            target="2016"
        )
    ]
}


spec_0prhtod4tli879nh = {
    "ops":[
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Population in millions",
            seriesField="City",
            by="Year",
            groupA="2010",
            groupB="2025"
        )
    ],
    "ops2":[
        SortOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Population in millions",
        )
    ],
    "ops3":[
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Population in millions",
            which="max"
        )
    ]
}


spec_2jki13q54zizc6i4 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["Jul 2008 - Jun 2009", "Jul 2009 - Jun 2010", "Jul 2010 - Jun 2011", "Jul 2011 - Jun 2012"]
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Number of trucks"
        ),
        ScaleOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            target="ref:n2",
            factor=1/4
        )
    ],
    "ops2":[
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Year",
            include=["Jul 2013 - Jun 2014", "Jul 2014 - Jun 2015", "Jul 2015 - Jun 2016", "Jul 2016 - Jun 2017"]
        ),
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            field="Number of trucks"
        ),
        ScaleOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=2),
            target="ref:n5",
            factor=1/4
        )
    ],
    "ops3":[
        CompareOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n3", "n6"], sentenceIndex=3),
            field="Number of trucks",
            targetA="ref:n3",
            targetB="ref:n6"
        )
    ]
}


spec_0pzdf7hfbxgjghsa = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2016"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2017"]
        ),
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=1),
            field="Production in billion heads",
            targetA="ref:n1",
            targetB="ref:n2"
        ),
        
    ],
    "ops2": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2018"]
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=2),
            field="Production in billion heads",
            targetA="ref:n2",
            targetB="ref:n4"
        ),
    ],
    "ops3":[
        CompareOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n4", "n5"], sentenceIndex=3),
            field="Production in billion heads",
            targetA="ref:n4",
            targetB="ref:n5"
        )
    ]
}


spec_0rfuaawgi58ajpsv = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Region",
            group="North America"
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Media rights revenue in billion US dollars",
        ),
        ScaleOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            target="ref:n2",
            factor=1/4
        )
    ],
    "ops2":[
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Region",
            group="Latin America"
        ),
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=3),
            field="Media rights revenue in billion US dollars",
        ),
        ScaleOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=3),
            target="ref:n5",
            factor=1/4
        )
    ],
    "ops3":[
        DiffOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n3", "n6"], sentenceIndex=3),
            field="Media rights revenue in billion US dollars",
            targetA="ref:n3",
            targetB="ref:n6"
        )
    ]
}


spec_0rdpculfpyw3bv5p = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Value in billion US dollars",
            by="Type",
            groupA="Lending",
            groupB="Investment"
        )
    ],
    "ops2":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Value in billion US dollars",
            which="min"
        )
    ],
    "ops3":[

    ]
}


spec_10x2rgiqw97wdspi = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Revenue_Type",
            group="Broadcasting"
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Revenue_Million_Euros"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3",inputs=[], sentenceIndex=1),
            field="Revenue_Type",
            group="Commercial"
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Revenue_Million_Euros"
        ),
    ],
    "ops2":[
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1", "n2"], sentenceIndex=2),
            field="Revenue_Million_Euros",
            operator=">",
            value="ref:n2"
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n3", "n4"], sentenceIndex=2),
            field="Revenue_Million_Euros",
            operator=">",
            value="ref:n4",
        ),
    ],
    "ops3": [
        
    ]
}


spec_0qz3v0bszsex7jjm ={
    "ops":[
        SumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Expenditure in billion GBP"
        ),
        ScaleOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            target="ref:n1",
            factor=1/19
        )
    ],
    "ops2":[
        FilterOp(
        id="n3",
        meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
        field="Expenditure in billion GBP",
        operator="<",
        value="ref:n2"
    )
    ],
    "ops3": [
        
    ]
}


spec_23wg8zio5ahp40tg = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Percentage",
            by="Year",
            groupA="Oppose",
            groupB="Favor"
        )
    ],
    "ops2":[
        
    ],
    "ops3":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=3),
            field="Percentage",
            which="max"
        )
    ]
}


spec_28bxxhd6omv2l2h1 = {
    "ops":[
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Life expectancy in years",
            by="Region",
            groupA="Canada",
            groupB="Newfoundland and Labrador"
        )
    ],
    "ops2":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Life expectancy in years",
            which="max"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Life expectancy in years",
            which="min"
        ),
    ],
    "ops3":[
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=4),
            field="Life expectancy in years",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ]
}


spec_29rxoltwhongoday = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Percentage",
            include=["2002"]
        ),
        DiffOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Percentage",
            groupA="Dissatisfied",
            groupB="Satisfied"
        )
    ],
    "ops2":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Percentage",
            include=["2017"]
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Percentage",
            groupA="Dissatisfied",
            groupB="Satisfied"
        )
    ],
    "ops3":[
        CompareOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Percentage",
            targetA="ref:n2",
            targetB="ref:n4",
            which="max"
        )
    ]
}


spec_2eiyyw562tcvjypp = {
    "ops":[
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Favorable View (%)",
            by="Year",
            seriesField="Country",
            groupA="US",
            groupB="Russia",
            signed=True
        )
    ],
    "ops2":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Country",
            operator="<",
            value=0
        )
    ],
    "ops3":[
        CountOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Year"
        )
    ]
}


spec_221xwpab655f7g8x = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2009"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Revenue_Million_Euros",
            group="0–14 years"
        )
    ],
    "ops2":[
        
    ],
    "ops3":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
            field="Year",
            include=["2019"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            field="Share of total population",
            group="65 years and older"
        ),
        
    ],
    "ops4":[

    ],
    "ops5":[
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=5),
            field="Share of total population",
            targetA="ref:n4",
            targetB="ref:n2"
        )
    ]
}


spec_23an1hozb7myw4e2 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share_of_Revenue",
            group="Men's apparel"
        ),
    ],
    "ops2":[
        
    ],
    "ops3":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=3),
            field="year",
            include=["2015"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=3),
            field="year",
            include=["2016"]
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=3),
            field="Share_of_Revenue",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ],
    "ops4":[
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1"], sentenceIndex=3),
            field="year",
            include=["2017"]
        ),
        DiffOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n3", "n5"], sentenceIndex=3),
            field="Share_of_Revenue",
            targetA="ref:n3",
            targetB="ref:n5"
        )
    ]
}


spec_4wqpl5jrdmc75go3 = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2025"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            group="Direct contribution"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            group="Total contribution"
        ),
    ],
    "ops2":[
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=2),
            field="Economic_Impact_Billion_USD",
        )
    ],
    "ops3":[
        ScaleOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            target="ref:n4",
            factor=1/2
        )
    ]
}


spec_74p313e1n8rzkfzp = {
    "ops":[
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share of respondents",
        )
    ],
    "ops2":[
        
    ],
    "ops3": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=3),
            field="Share of respondents",
            which="max"
        )
    ]
}


spec_7mgydgux0ay0flv4 = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2003", "2004", "2005"]
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2004", "2005", "2006"]
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2005", "2006", "2007"]
        ),
        AverageOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2006", "2007", "2008"]
        ),
        AverageOp(
            id="n8",
            meta=OpsMeta(nodeId="n7", inputs=["n7"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2007", "2008", "2009"]
        ),
        AverageOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n9"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2009", "2010", "2011"]
        ),
        AverageOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n11"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2010", "2011", "2012"]
        ),
        AverageOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n13"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2011", "2012", "2013"]
        ),
        AverageOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=["n15"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2012", "2013", "2014"]
        ),
        AverageOp(
            id="n18",
            meta=OpsMeta(nodeId="n16", inputs=["n17"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2013", "2014", "2015"]
        ),
        AverageOp(
            id="n20",
            meta=OpsMeta(nodeId="n16", inputs=["n19"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n21",
            meta=OpsMeta(nodeId="n21", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2015", "2016", "2017"]
        ),
        AverageOp(
            id="n22",
            meta=OpsMeta(nodeId="n22", inputs=["n21"], sentenceIndex=1),
            field="Number of units sold"
        ),
        FilterOp(
            id="n23",
            meta=OpsMeta(nodeId="n23", inputs=[], sentenceIndex=1),
            field="Year",
            include = ["2017", "2018", "2019"]
        ),
        AverageOp(
            id="n24",
            meta=OpsMeta(nodeId="n24", inputs=["n23"], sentenceIndex=1),
            field="Number of units sold"
        ),
    ],
    "ops2":[
        
    ],
    "ops3":[
        FindExtremumOp(
            id="n25",
            meta=OpsMeta(nodeId="n25", inputs=["n2", "n4", "n6", "n8", "n10", "n12", "n14", "n16", "n18", "n20", "n22", "24"], sentenceIndex=3),
            field="Number of units sold",
            which="max"
        )
    ]
}

spec_4pi1e6ev8e0zobww = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Gender",
            group="Male"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Year",
            include=["2009", "2010", "2011"]
        ),
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            field="Population"
        )
    ],
    "ops2": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Gender",
            group="Female"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2018", "2019", "2020"]
        ),
        AverageOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=2),
            field="Population"
        )
    ],
    "ops3": [
        DiffOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n3", "n6"], sentenceIndex=2),
            field="Population",
            targetA="ref:n3",
            targetB="ref:n6"
        ),
    ],
}

spec_1gb8sqnptdsdvagz = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Age Group",
            group="Under 30s"
        )
    ],
    "ops2":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Share of respondents",
            operator="<",
            value=0.10
        )
    ],
    "ops3":[

    ]
}


spec_4vcdm7lwwlgdd0h1 = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Median_Wealth_Million_USD",
            by="Year",
            groupA="Senate",
            groupB="House"
        )
    ],
    "ops2":[
        
    ],
    "ops3": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=3),
            field="Median_Wealth_Million_USD",
            which="min"
        )
    ]
}


spec_1hm2mi3o0ejxp7tn = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Normotensive untreated"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Hypertensive controlled"
        ),
        
    ],
    "ops2":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Gender",
            group="Men"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=2),
            field="Gender",
            group="Women"
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=2),
            field="Share of respondents",
            targetA="ref:n3",
            targetB="ref:n2"
        )
    ],
    "ops3":[
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2"], sentenceIndex=3),
            field="Gender",
            group="Men"
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n2"], sentenceIndex=3),
            field="Gender",
            group="Women"
        ),
        DiffOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n5", "n6"], sentenceIndex=3),
            field="Share of respondents",
            targetA="ref:n5",
            targetB="ref:n6"
        )
    ],
    "ops4": [

    ]
}


spec_240rurpp2arislnt = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Age Group",
            include=["18–29"]
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Share of respondents",
            which="min"
        )
    ],
    "ops2":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Age Group",
            include=["65+"]
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Share of respondents",
            which="max"
        )
    ],
    "ops3":[
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Share of respondents",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ],
    "ops4":[

    ],
    "ops5":[
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=5),
            group="Don't know/ No opinion"
        )
    ],
    "ops6":[

    ],
    "ops7":[
        
    ],
    "ops8":[

    ],
    "ops9":[

    ],
    "ops10":[

    ],
    "ops11":[
        
    ]
}


spec_2a8mliwolqqo6s5u = {
    "ops":[
        # 2013
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2013"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Region",
            exclude=["Asia Pacific"]
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            field="Market_Size_Billion_USD"
        ),
        # 2014
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2014"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=1),
            field="Region",
            exclude=["Asia Pacific"]
        ),
        SumOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=1),
            field="Market_Size_Billion_USD"
        ),
        # 2015
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2015"]
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n7"], sentenceIndex=1),
            field="Region",
            exclude=["Asia Pacific"]
        ),
        SumOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n8"], sentenceIndex=1),
            field="Market_Size_Billion_USD"
        ),
        # 2016
        FilterOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2016"]
        ),
        FilterOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n10"], sentenceIndex=1),
            field="Region",
            exclude=["Asia Pacific"]
        ),
        SumOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n11"], sentenceIndex=1),
            field="Market_Size_Billion_USD"
        ),
        # 2017
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2017"]
        ),
        FilterOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n13"], sentenceIndex=1),
            field="Region",
            exclude=["Asia Pacific"]
        ),
        SumOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=["n14"], sentenceIndex=1),
            field="Market_Size_Billion_USD"
        ),
        # 2018
        FilterOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2018"]
        ),
        FilterOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=["n16"], sentenceIndex=1),
            field="Region",
            exclude=["Asia Pacific"]
        ),
        SumOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=["n17"], sentenceIndex=1),
            field="Market_Size_Billion_USD"
        ),
        # 2019
        FilterOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2019"]
        ),
        FilterOp(
            id="n20",
            meta=OpsMeta(nodeId="n20", inputs=["n19"], sentenceIndex=1),
            field="Region",
            exclude=["Asia Pacific"]
        ),
        SumOp(
            id="n21",
            meta=OpsMeta(nodeId="n21", inputs=["n20"], sentenceIndex=1),
            field="Market_Size_Billion_USD"
        ),
        # 2020
        FilterOp(
            id="n22",
            meta=OpsMeta(nodeId="n22", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2020"]
        ),
        FilterOp(
            id="n23",
            meta=OpsMeta(nodeId="n23", inputs=["n22"], sentenceIndex=1),
            field="Region",
            exclude=["Asia Pacific"]
        ),
        SumOp(
            id="n24",
            meta=OpsMeta(nodeId="n24", inputs=["n23"], sentenceIndex=1),
            field="Market_Size_Billion_USD"
        ),
        # 2021
        FilterOp(
            id="n25",
            meta=OpsMeta(nodeId="n25", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2021"]
        ),
        FilterOp(
            id="n26",
            meta=OpsMeta(nodeId="n26", inputs=["n25"], sentenceIndex=1),
            field="Region",
            exclude=["Asia Pacific"]
        ),
        SumOp(
            id="n27",
            meta=OpsMeta(nodeId="n27", inputs=["n26"], sentenceIndex=1),
            field="Market_Size_Billion_USD"
        ),
    ],
    "ops2":[
        FilterOp(
            id="n28",
            meta=OpsMeta(nodeId="n28", inputs=[], sentenceIndex=2),
            field="Region",
            group="Asia Pacific"
        ),
        FilterOp(
            id="n29",
            meta=OpsMeta(nodeId="n1", inputs=["n28"], sentenceIndex=2),
            field="Year",
            include=["2013"]
        ),
        FilterOp(
            id="n30",
            meta=OpsMeta(nodeId="n30", inputs=["n28"], sentenceIndex=2),
            field="Year",
            include=["2014"]
        ),
        FilterOp(
            id="n31",
            meta=OpsMeta(nodeId="n31", inputs=["n28"], sentenceIndex=2),
            field="Year",
            include=["2015"]
        ),
        FilterOp(
            id="n32",
            meta=OpsMeta(nodeId="n32", inputs=["n28"], sentenceIndex=2),
            field="Year",
            include=["2016"]
        ),
        FilterOp(
            id="n33",
            meta=OpsMeta(nodeId="n33", inputs=["n28"], sentenceIndex=2),
            field="Year",
            include=["2017"]
        ),
        FilterOp(
            id="n34",
            meta=OpsMeta(nodeId="n34", inputs=["n28"], sentenceIndex=2),
            field="Year",
            include=["2018"]
        ),
        FilterOp(
            id="n35",
            meta=OpsMeta(nodeId="n35", inputs=["n28"], sentenceIndex=2),
            field="Year",
            include=["2019"]
        ),
        FilterOp(
            id="n36",
            meta=OpsMeta(nodeId="n36", inputs=["n28"], sentenceIndex=2),
            field="Year",
            include=["2020"]
        ),
        FilterOp(
            id="n37",
            meta=OpsMeta(nodeId="n37", inputs=["n28"], sentenceIndex=2),
            field="Year",
            include=["2021"]
        ),
        DiffOp(
            id="n38",
            meta=OpsMeta(nodeId="n38", inputs=["n3", "n29"], sentenceIndex=2),
            field="Market_Size_Billion_USD",
            targetA="ref:n3",
            targetB="ref:n29"
        ),
        DiffOp(
            id="n39",
            meta=OpsMeta(nodeId="n39", inputs=["n6", "n30"], sentenceIndex=2),
            field="Market_Size_Billion_USD",
            targetA="ref:n6",
            targetB="ref:n30"
        ),
        DiffOp(
            id="n40",
            meta=OpsMeta(nodeId="n38", inputs=["n9", "n31"], sentenceIndex=2),
            field="Market_Size_Billion_USD",
            targetA="ref:n9",
            targetB="ref:n31"
        ),
        DiffOp(
            id="41",
            meta=OpsMeta(nodeId="n41", inputs=["n12", "n32"], sentenceIndex=2),
            field="Market_Size_Billion_USD",
            targetA="ref:n12",
            targetB="ref:n32"
        ),
        DiffOp(
            id="n42",
            meta=OpsMeta(nodeId="n42", inputs=["n15", "n33"], sentenceIndex=2),
            field="Market_Size_Billion_USD",
            targetA="ref:n15",
            targetB="ref:n33"
        ),
        DiffOp(
            id="n43",
            meta=OpsMeta(nodeId="n43", inputs=["n18", "n34"], sentenceIndex=2),
            field="Market_Size_Billion_USD",
            targetA="ref:n18",
            targetB="ref:n34"
        ),
        DiffOp(
            id="n44",
            meta=OpsMeta(nodeId="n38", inputs=["n21", "n35"], sentenceIndex=2),
            field="Market_Size_Billion_USD",
            targetA="ref:n21",
            targetB="ref:n35"
        ),
        DiffOp(
            id="n45",
            meta=OpsMeta(nodeId="n45", inputs=["n24", "n36"], sentenceIndex=2),
            field="Market_Size_Billion_USD",
            targetA="ref:n24",
            targetB="ref:n30"
        ),
    ],
    "ops3":[
        FindExtremumOp(
            id="n46",
            meta=OpsMeta(nodeId="n46", inputs=["n39", "n40", "n41", "n42", "n43", "n44", "n45"], sentenceIndex=3),
            field="Market_Size_Billion_USD",
            which="min"
        )
    ]
}

# 확인


spec_1a6pxfig1xf4oeu3 = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2006"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2007"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2008"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2009"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2010"]
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2011"]
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2012"]
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2013"]
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2014"]
        ),
        FilterOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2015"]
        ),
        FilterOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2016"]
        ),
        FilterOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2017"]
        ),
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2018"]
        ),
        FilterOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2019"]
        ),
        FilterOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=[], sentenceIndex=1),
            field="Year",
            value=["2020"]
        ),
    ],
    "ops2":[
        FilterOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=[], sentenceIndex=2),
            field="Franchise value in million US dollars",
            operator="<=",
            value=200
        )
    ],
    "ops3":[
        FilterOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=[], sentenceIndex=2),
            field="Year",
            operator="between",
            value=["2006", "2012"]
        )
    ]
}


spec_1ashoniy42n3n5jr = {
    "ops": [
        AverageOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Operating revenue in m million NOK"
        )
    ],
    "ops2":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Year",
            exclude=["2020"]
        ),
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Operating revenue in m million NOK"
        )
    ],
    "ops3":[
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1", "n3"], sentenceIndex=3),
            field="Operating revenue in m million NOK",
            targetA="ref:n3",
            targetB="ref:n1",
            signed=True
        )
    ]
}


spec_4twwx65oath7vrkt = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Trade_Type",
            group="Imports"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Value_Trillion_USD",
            which="min"
        ),
        RetrieveValueOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            field="Value_Trillion_USD",
            target=1.15
        )
    ],
    "ops2":[
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Trade_Type",
            group="Exports"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2000"]
        ),
        CompareOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n5",
            targetB=1.15,

        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2001"]
        ),
        CompareOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n7"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n7",
            targetB=1.15
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2002"]
        ),
        CompareOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n9"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n9",
            targetB=1.15
        ),
        FilterOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2003"]
        ),
        CompareOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n11"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n11",
            targetB=1.15
        ),
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2004"]
        ),
        CompareOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n13"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n13",
            targetB=1.15
        ),
        FilterOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2005"]
        ),
        CompareOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=["n15"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n15",
            targetB=1.15
        ),
        FilterOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2006"]
        ),
        CompareOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=["n17"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n17",
            targetB=1.15
        ),
        FilterOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2007"]
        ),
        CompareOp(
            id="n20",
            meta=OpsMeta(nodeId="n20", inputs=["n19"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n19",
            targetB=1.15
        ),
        FilterOp(
            id="n21",
            meta=OpsMeta(nodeId="n21", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2008"]
        ),
        CompareOp(
            id="n22",
            meta=OpsMeta(nodeId="n22", inputs=["n21"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n21",
            targetB=1.15
        ),
        FilterOp(
            id="n23",
            meta=OpsMeta(nodeId="n23", inputs=["n22"], sentenceIndex=2),
            field="Year",
            include=["2009"]
        ),
        CompareOp(
            id="n24",
            meta=OpsMeta(nodeId="n24", inputs=["n23"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n23",
            targetB=1.15
        ),
        FilterOp(
            id="n25",
            meta=OpsMeta(nodeId="n25", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2010"]
        ),
        CompareOp(
            id="n26",
            meta=OpsMeta(nodeId="n14", inputs=["n25"], sentenceIndex=2),
            field="Value_Trillion_USD",
            targetA="ref:n25",
            targetB=1.15
        ),
        FilterOp(
            id="n27",
            meta=OpsMeta(nodeId="n27", inputs=["n4"], sentenceIndex=2),
            field="Year",
            include=["2011"]
        ),
    ],
    "ops3":[
        
    ],
    "ops4":[
        FilterOp(
            id="n28",
            meta=OpsMeta(nodeId="n28", inputs=[], sentenceIndex=4),
            field="Year",
            operator="between",
            value=["2004", "2011"]
        )
    ]
}


spec_1ar60b8rke2d8e64 = {
    "ops":[
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Retention rate",
            by="Type",
            groupA="Average",
            groupB="Messaging apps"
        )
    ],
    "ops2":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Retention rate",
            which="min"
        )
    ],
    "ops3":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
            field="Time Period",
            include=["12th month"]
        )
    ]
}


spec_7w9v4fsbg5ydxsr2 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2009", "2011", "2013", "2015", "2017"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Year",
            exclude=["2009", "2011", "2013", "2015", "2017"]
        )
    ],
    "ops2": [
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Percentage of gross domestic product",
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=2),
            field="Percentage of gross domestic product",
        )
    ],
    "ops3":[
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3", "n4"], sentenceIndex=3),
            field="Percentage of gross domestic product",
            targetA="ref:n3",
            targetB="ref:n4"
        )
    ]
}


spec_1a09xqtrj8zms716 = {
    "ops": [
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="US dollars per square foot",
            which="max",
            rank=1
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="US dollars per square foot",
            which="max",
            rank=2
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="US dollars per square foot",
            which="max",
            rank=3
        ),
    ],
    "ops2":[
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1", "n2", "n3"], sentenceIndex=2),
            field="US dollars per square foot"
        ),
        ScaleOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            target="ref:n4",
            factor=1/3
        )
    ]
}


spec_1bbe64wpvq06sknm = {
    "ops":[
        SumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Number of days in thousands"
        ),
        ScaleOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            target="ref:n1",
            factor=1/9
        )
    ],
    "ops2":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["2010/11"]
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=2),
            field="Number of days in thousands",
            targetA="ref:n2",
            targetB="ref:n3",
            signed=True
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["2011/12"]
        ),
        DiffOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n2", "n5"], sentenceIndex=2),
            field="Number of days in thousands",
            targetA="ref:n2",
            targetB="ref:n5",
            signed=True
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["2013/14"]
        ),
        DiffOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n2", "n7"], sentenceIndex=2),
            field="Number of days in thousands",
            targetA="ref:n2",
            targetB="ref:n7",
            signed=True
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["2014/15"]
        ),
        DiffOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n2", "n9"], sentenceIndex=2),
            field="Number of days in thousands",
            targetA="ref:n2",
            targetB="ref:n9",
            signed=True
        ),
        FilterOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["2015/16"]
        ),
        DiffOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n2", "n11"], sentenceIndex=2),
            field="Number of days in thousands",
            targetA="ref:n2",
            targetB="ref:n11",
            signed=True
        ),
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["2016/17"]
        ),
        DiffOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n2", "n13"], sentenceIndex=2),
            field="Number of days in thousands",
            targetA="ref:n2",
            targetB="ref:n13",
            signed=True
        ),
        FilterOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["2016/17"]
        ),
        DiffOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=["n2", "n15"], sentenceIndex=2),
            field="Number of days in thousands",
            targetA="ref:n2",
            targetB="ref:n15",
            signed=True
        ),
        FilterOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["2017/18"]
        ),
        DiffOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=["n2", "n17"], sentenceIndex=2),
            field="Number of days in thousands",
            targetA="ref:n2",
            targetB="ref:n17",
            signed=True
        ),
        FilterOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["2018/19"]
        ),
        DiffOp(
            id="n20",
            meta=OpsMeta(nodeId="n20", inputs=["n2", "n19"], sentenceIndex=2),
            field="Number of days in thousands",
            targetA="ref:n2",
            targetB="ref:n19",
            signed=True
        ),
    ]
}


spec_16fif5hdi8yzml00 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Maximum"
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Payment_Million_USD"
        )
    ],
    "ops2":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            group="Minimum"
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Payment_Million_USD"
        )
    ],
    "ops3":[
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Payment_Million_USD",
            targetA="ref:n4",
            targetB="ref:n2"
        )
    ]
}


spec_827lhm2w7n652knp = {
    "ops":[
        
    ],
    "ops2":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=2),
            field="Year",
            operator="between",
            value=["2007", "2008"]
        )
    ],
    "ops3":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=3),
            field="Year",
            operator="between",
            value=["2009", "2011"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
            field="Year",
            include=["2012"]
        ),
        
    ],
    "ops4":[
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=4),
            field="Year",
            include=["2008", "2012"]
        ),
        CountOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=4),
            field="Year"
        )
    ]
}


spec_12sdcc2xjltg7qj2 = {
    "ops":[
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Value_Million_USD",
            by="Year",
            seriesField="Category",
            groupA="Total contributions to presidential candidates",
            groupB="Total spending by presidential candidates"
        )
    ],
    "ops2":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Value_Million_USD",
            which="max"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Value_Million_USD",
            which="min"
        )
    ],
    "ops3":[
        # ScaleOp(
        #     id="n4",
        #     meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=2),
        #     target="ref:n2",
        #     factor=1/int("ref:n3")
        # )
    ]
}


spec_72yqb8jwj9a6g4nx = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2005", "2006", "2007", "2008", "2009", "2010"]
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Percentage of internet users"
        )
    ],
    "ops2":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2011"]
        )
    ],
    "ops3":[
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=3),
            field="Percentage of internet users",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ]
}


spec_6al86e9qyokma74i = {
    "ops": [
        AverageOp(
            id="n1",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Number of renunciations"
        )
    ],
    "ops2":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2008"]
        ),
        CompareBoolOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=2),
            targetA="ref:n1",
            targetB="ref:n2",
            operator=">"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2009"]
        ),
        CompareBoolOp(
            id="n4",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n3"], sentenceIndex=2),
            targetA="ref:n1",
            targetB="ref:n3",
            operator=">"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2010"]
        ),
        CompareBoolOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1", "n5"], sentenceIndex=2),
            targetA="ref:n1",
            targetB="ref:n5",
            operator=">"
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2011"]
        ),
        CompareBoolOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n1", "n7"], sentenceIndex=2),
            targetA="ref:n1",
            targetB="ref:n7",
            operator=">"
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2012"]
        ),
        CompareBoolOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n1", "n9"], sentenceIndex=2),
            targetA="ref:n1",
            targetB="ref:n9",
            operator=">"
        ),
        FilterOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2013"]
        ),
        CompareBoolOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n1", "n11"], sentenceIndex=2),
            targetA="ref:n1",
            targetB="ref:n11",
            operator=">"
        ),
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2014"]
        ),
        CompareBoolOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n1", "n13"], sentenceIndex=2),
            targetA="ref:n1",
            targetB="ref:n13",
            operator=">"
        ),
        FilterOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2015"]
        ),
        CompareBoolOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=["n1", "n15"], sentenceIndex=2),
            targetA="ref:n1",
            targetB="ref:n15",
            operator=">"
        ),
    ],
    "ops3":[
        FilterOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=["n1"], sentenceIndex=3),
            field="Number of renunciations",
            operator="<",
            value="ref:n1"
        ),
        CountOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=["n17"], sentenceIndex=3),
            field="Year"
        )
    ]
}


spec_724mfnyk34kp97le = {
    "ops":[
        SumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Cinema visits in millions"
        ),
        ScaleOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            target="ref:n1",
            factor=1/19
        )
    ],
    "ops2":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2001"]
        ),
        CompareBoolOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n3",
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2002"]
        ),
        CompareBoolOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n2", "n5"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n5"
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2003"]
        ),
        CompareBoolOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n2", "n7"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n7"
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2004"]
        ),
        CompareOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n2", "n9"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n9",
            which="min"
        ),
        FilterOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2005"]
        ),
        CompareBoolOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n2", "n11"], sentenceIndex=2),
            targetA="ref:n1",
            targetB="ref:n9"
        ),
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2006"]
        ),
        CompareOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n2", "n13"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n13",
            which="min"
        ),
        FilterOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2007"]
        ),
        CompareOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=["n2", "n15"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n15",
            which="min"
        ),
        FilterOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2008"]
        ),
        CompareOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=["n2", "n17"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n17",
            which="min"
        ),
        FilterOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2009"]
        ),
        CompareOp(
            id="n20",
            meta=OpsMeta(nodeId="n20", inputs=["n2", "n19"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n19",
            which="min"
        ),
        FilterOp(
            id="n21",
            meta=OpsMeta(nodeId="n21", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2010"]
        ),
        CompareOp(
            id="n22",
            meta=OpsMeta(nodeId="n22", inputs=["n2", "n21"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n21",
            which="min"
        ),
        FilterOp(
            id="n23",
            meta=OpsMeta(nodeId="n23", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2011"]
        ),
        CompareOp(
            id="n24",
            meta=OpsMeta(nodeId="n24", inputs=["n2", "n23"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n23",
            which="min"
        ),
        FilterOp(
            id="n25",
            meta=OpsMeta(nodeId="n25", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2012"]
        ),
        CompareOp(
            id="n26",
            meta=OpsMeta(nodeId="n26", inputs=["n2", "n25"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n25",
            which="min"
        ),
        FilterOp(
            id="n27",
            meta=OpsMeta(nodeId="n27", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2013"]
        ),
        CompareOp(
            id="n28",
            meta=OpsMeta(nodeId="n28", inputs=["n2", "n28"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n28",
            which="min"
        ),
        FilterOp(
            id="n29",
            meta=OpsMeta(nodeId="n29", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2014"]
        ),
        CompareOp(
            id="n30",
            meta=OpsMeta(nodeId="n30", inputs=["n2", "n29"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n29",
            which="min"
        ),
        FilterOp(
            id="n31",
            meta=OpsMeta(nodeId="n31", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2015"]
        ),
        CompareOp(
            id="n32",
            meta=OpsMeta(nodeId="n32", inputs=["n2", "n32"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n32",
            which="min"
        ),
        FilterOp(
            id="n33",
            meta=OpsMeta(nodeId="n33", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2017"]
        ),
        CompareOp(
            id="n34",
            meta=OpsMeta(nodeId="n34", inputs=["n2", "n34"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n34",
            which="min"
        ),
        FilterOp(
            id="n35",
            meta=OpsMeta(nodeId="n35", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2018"]
        ),
        CompareOp(
            id="n36",
            meta=OpsMeta(nodeId="n36", inputs=["n2", "n36"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n36",
            which="min"
        ),
        FilterOp(
            id="n37",
            meta=OpsMeta(nodeId="n37", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2019"]
        ),
        CompareOp(
            id="n38",
            meta=OpsMeta(nodeId="n38", inputs=["n2", "n38"], sentenceIndex=2),
            targetA="ref:n2",
            targetB="ref:n38",
            which="min"
        ),
    ],
    "ops3":[
        FilterOp(
            id="n39",
            meta=OpsMeta(nodeId="n39", inputs=["n2"], sentenceIndex=3),
            field="Cinema visits in millions",
            operator="<",
            value="ref:n2"
        ),
        CountOp(
            id="n40",
            meta=OpsMeta(nodeId="n40", inputs=["n39"], sentenceIndex=3),
            field="Year"
        )
    ]
}


spec_1q3mzgt77lwo172f = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="0 – 500 million US dollars"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            group="Over 10,001 million U.S. dollars"
        )
    ],
    "ops2":[
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=2),
            field="Market share",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ],
    "ops3":[
        
    ],
    "ops4": [
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=4),
            field="Market share",
            which="max"
        )
    ]
}


spec_0xo3r87obscjsktm = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Country",
            include=["El Salvador"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Country",
            include=["Ukraine"]
        ),
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=2),
            field="Mortality, Per 1 000 000 Inhabitants, 1997",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ],
    "ops2":[
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=1),
            field="Country",
            include=["Denmark"]
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1", "n3"], sentenceIndex=2),
            field="Mortality, Per 1 000 000 Inhabitants, 1997",
            targetA="ref:n1",
            targetB="ref:n3"
        )
    ],
    "ops3":[
        ScaleOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1", "n2"], sentenceIndex=3),
            target="ref:n1",
            factor=1/380
        )
    ]
}


spec_0ykydh8vao50ceou = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Channel",
            include=["Brokers"]
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Share of total gross premiums written",
            which="max"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Share of total gross premiums written",
            which="min"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=1),
            field="Channel",
            include=["Direct writing"]
        ),
        FindExtremumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=1),
            field="Share of total gross premiums written",
            which="max"
        ),
        FindExtremumOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n4"], sentenceIndex=1),
            field="Share of total gross premiums written",
            which="min"
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=1),
            field="Channel",
            include=["Agents"]
        ),
        FindExtremumOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n7"], sentenceIndex=1),
            field="Share of total gross premiums written",
            which="max"
        ),
        FindExtremumOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n7"], sentenceIndex=1),
            field="Share of total gross premiums written",
            which="min"         
        ),
        FilterOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=[], sentenceIndex=1),
            field="Channel",
            include=["Bancassurance"]
        ),
        FindExtremumOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n10"], sentenceIndex=1),
            field="Share of total gross premiums written",
            which="max"
        ),
        FindExtremumOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n10"], sentenceIndex=1),
            field="Share of total gross premiums written",
            which="min"
        )
    ],
    "ops2":[
        DiffOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n2", "n3"], sentenceIndex=2),
            field="Share of total gross premiums written",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        DiffOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=["n5", "n6"], sentenceIndex=2),
            field="Share of total gross premiums written",
            targetA="ref:n5",
            targetB="ref:n6"
        ),
        DiffOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n8", "n9"], sentenceIndex=2),
            field="Share of total gross premiums written",
            targetA="ref:n8",
            targetB="ref:n9"
        ),
        DiffOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=["n11", "n12"], sentenceIndex=2),
            field="Share of total gross premiums written",
            targetA="ref:n11",
            targetB="ref:n12"
        )
    ],
    "ops3":[
        FindExtremumOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=["n12", "n13", "n14", "n15"], sentenceIndex=2),
            field="Share of total gross premiums written",
            which="max"
        )
    ],
    "ops4":[

    ]
}


spec_4p1m4tsmzmtvsrys = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share_of_Respondents",
            by="Date_Range",
            groupA="Obama",
            groupB="Romney",
            signed=True
        )
    ],
    "ops2":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Share_of_Respondents",
            operator=">",
            value=0
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Share_of_Respondents",
            operator="<",
            value=0
        )
    ],
    "ops3":[
        CountOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=1),
            field="Date_Range"
        ),
        CountOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3"], sentenceIndex=2),
            field="Date_Range"
        ),
        DiffOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n3", "n5"], sentenceIndex=3),
            field="Date_Range",
            targetA="ref:n3",
            targetB="ref:n5"
        )
    ]
}


spec_0wflwm4jebx7n12y = {
    "ops":[
        SumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Number of fires"
        ),
        ScaleOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            target="ref:n1",
            factor=1/16
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Number of fires",
            which="max"
        )
    ],
    "ops3":[
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1", "n3"], sentenceIndex=3),
            field="Number of fires",
            targetA="ref:n3",
            targetB="ref:n1"
        )
    ]
}


spec_21fa7gb8l1ix6yfm = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Frequency",
            value="EVERY DAY"
        ),
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Frequency",
            value="LESS OFTEN"
        ),
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=1),
            field="Share_of_Respondents"
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            field="Share_of_Respondents",
        )
    ]
}


spec_0zjxkqy20iibpdvo = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Platform",
            include=["YouTube", "Twitter", "Twitch"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Platform",
            include=["Facebook", "Instagram", "Snapchat", "TikTok"]
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Gender",
            operator="==",
            value="Female"
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Share of respondents"
        )
    ],
    "ops3": [
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=3),
            field="Gender",
            operator="==",
            value="Male"
        ),
        AverageOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=3),
            field="Share of respondents"
        )
    ],
    "ops4": [
        
    ],
    "ops5": [
        
    ], 
    "ops6":[

    ],
    "ops7":[

    ],
    "ops8":[
        DiffOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n3", "n6"], sentenceIndex=8),
            field="Share of respondents",
            targetA="ref:n6",
            targetB="ref:n3"
        )
    ],
    "ops9":[

    ]
}


spec_0xnim79vztf8hjor = {
    "ops":[
        AverageOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Average ticket price in US dollars"
        )
    ],
    "ops2":[
        # 05/06
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["05/06"]
        ),
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n1",
            targetB="ref:n2"
        ),
        # 06/07
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["06/07"]
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1", "n4"], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n1",
            targetB="ref:n4"
        ),
        # 07/08
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["07/08"]
        ),
        DiffOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n1", "n6"], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n1",
            targetB="ref:n6"
        ),
        # 08/09
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["08/09"]
        ),
        DiffOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n1", "n8"], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n1",
            targetB="ref:n8"
        ),
        # 09/10
        FilterOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["09/10"]
        ),
        DiffOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n1", "n10"], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n1",
            targetB="ref:n10"
        ),
        # 10/11
        FilterOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["10/11"]
        ),
        DiffOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=["n1", "n12"], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n1",
            targetB="ref:n12"
        ),
        # 11/12
        FilterOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["11/12"]
        ),
        DiffOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=["n1", "n14"], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n1",
            targetB="ref:n14"
        ),
        # 12/13
        FilterOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["12/13"]
        ),
        DiffOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=["n1", "n16"], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n1",
            targetB="ref:n15"
        ),
        # 13/14
        FilterOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["13/14"]
        ),
        DiffOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=["n1", "n18"], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n1",
            targetB="ref:n18"
        ),
        # 14/15
        FilterOp(
            id="n20",
            meta=OpsMeta(nodeId="n20", inputs=[], sentenceIndex=2),
            field="Fiscal Year",
            include=["14/15"]
        ),
        DiffOp(
            id="n21",
            meta=OpsMeta(nodeId="n19", inputs=["n1", "n20"], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n1",
            targetB="ref:n20"
        ),
    ],
    "ops3":[
        FindExtremumOp(
            id="n22",
            meta=OpsMeta(nodeId="n22", inputs=["n3", "n5", "n7", "n9", "n11", "n13", "n15", "n17", "n19", "n21"], sentenceIndex=3),
            field="Fiscal Year",
            which="max"
        )
    ]
}

 
spec_0w88bu7qm4ilsqmh = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["1995", "1999"]
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Installed base in million units"
        ),

    ],
    "ops2":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2010", "2013", "2017"]
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Installed base in million units"
        ),
    ],
    "ops3":[
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Installed base in million units",
            targetA="ref:n4",
            targetB="ref:n2"
        )
    ]
}


spec_0yx2080f08329xxb = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2009", "2010", "2011", "2012", "2013"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2014", "2015", "2016", "2017", "2018"]
        )
    ],
    "ops2":[
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Value market share"
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=2),
            field="Value market share"
        )
    ],
    "ops3":[
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3", "n4"], sentenceIndex=4),
            field="Value market share",
            targetA="ref:n3",
            targetB="ref:n4"
        )
    ]
}


spec_3z678inbp0t89ahu = {
    "ops":[
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Percentage_of_Respondents",
            by="Opinion",
            groupA="Dissatisfied",
            groupB="Satisfied",
        ),
        
    ],
    "ops2":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Percentage_of_Respondents",
            group="Dissatisfied"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Percentage_of_Respondents",
            group="Satisfied"
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=1),
            field="Percentage_of_Respondents"
        ),
        AverageOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3"], sentenceIndex=1),
            field="Percentage_of_Respondents"
        ),
        DiffOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n4", "n5"], sentenceIndex=2),
            field="Percentage_of_Respondents",
            targetA="ref:n4",
            targetB="ref:n5"
        )
    ],
    "ops3":[
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n1", "n6"], sentenceIndex=3),
            field="Percentage_of_Respondents",
            operator="<",
            value="ref:n6"
        )
    ]
}

# 확인
spec_3un2wyjae3ebkncl = {
    "ops":[
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share_of_Respondents",
            by="News_Source",
            groupA="Internet",
            groupB="Newspaper",
            signed=True
        ),
        PairDiffOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Share_of_Respondents",
            by="News_Source",
            groupA="Internet",
            groupB="Radio",
            signed=True
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Share_of_Respondents",
            operator=">",
            value=0
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=2),
            field="Share_of_Respondents",
            operator="<",
            value=0
        ),
        # union?
    ],
    "ops2":[
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            group="Internet"
        )
    ],
    "ops3":[
        AverageOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=3),
            field="Share_of_Respondents"
        )
    ]
}


spec_1xz4egh52kvh2xwx = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Canada",
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            group="Other International",
        ),
    ],
    "ops2":[
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=2),
            field="Total_Revenue_Million_USD"
        )
    ],
    "ops3":[
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=3),
            field="Year",
            include=["2020"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=3),
            group="US"
        )
    ],
    "ops4":[
        CompareOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n3", "n5"], sentenceIndex=3),
            field="Total_Revenue_Million_USD",
            targetA="ref:n3",
            targetB="ref:n5"
        )
    ]
}


spec_7272hodb02i6e09q = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            operator="between",
            value=["2007", "2013"]
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Population growth compared to previous year",
            which="max"
        )
    ],
    "ops2":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Year",
            operator="between",
            value=["2015", "2019"]
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n4"], sentenceIndex=2),
            field="Population growth compared to previous year",
            which="max"
        )
    ],
    "ops3":[
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Population growth compared to previous year",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}


spec_1y6itl6f2ho959ec = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group=["Approves", "No answer"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Country_Region",
            include=["Chile"]
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            field="Share_of_Respondents"
        )
    ],
    "ops2":[
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=2),
            field="Share_of_Respondents",
            exclude=["Chile"]
        ),
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            field="Share_of_Respondents"
        )
    ],
    "ops3": [
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Mexico"]
        ),
        CompareOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n2", "n6"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n6",
            which="max"
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Central America & Caribbean"]
        ),
        CompareOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n2", "n8"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n8",
            which="max"
        ),
        FilterOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Bolivia"]
        ),
        CompareOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n2", "n10"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n10",
            which="max"
        ),
        FilterOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Brazil"]
        ),
        CompareOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=["n2", "n12"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n12",
            which="max"
        ),
        FilterOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Central America & Caribbean"]
        ),
        CompareOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=["n2", "n14"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n14",
            which="max"
        ),
        FilterOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Bolivia"]
        ),
        CompareOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=["n2", "n16"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n16",
            which="max"
        ),
        FilterOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Peru"]
        ),
        CompareOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=["n2", "n18"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n18",
            which="max"
        ),
        FilterOp(
            id="n20",
            meta=OpsMeta(nodeId="n20", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Central America & Caribbean"]
        ),
        CompareOp(
            id="n21",
            meta=OpsMeta(nodeId="n21", inputs=["n2", "n20"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n20",
            which="max"
        ),
        FilterOp(
            id="n22",
            meta=OpsMeta(nodeId="n22", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Bolivia"]
        ),
        CompareOp(
            id="n23",
            meta=OpsMeta(nodeId="n23", inputs=["n2", "n22"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n22",
            which="max"
        ),
        FilterOp(
            id="n24",
            meta=OpsMeta(nodeId="n24", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Brazil"]
        ),
        CompareOp(
            id="n25",
            meta=OpsMeta(nodeId="n25", inputs=["n2", "n24"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n24",
            which="max"
        ),
        FilterOp(
            id="n26",
            meta=OpsMeta(nodeId="n26", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Central America & Caribbean"]
        ),
        CompareOp(
            id="n27",
            meta=OpsMeta(nodeId="n27", inputs=["n2", "n26"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n26",
            which="max"
        ),
        FilterOp(
            id="n28",
            meta=OpsMeta(nodeId="n28", inputs=["n1"], sentenceIndex=3),
            field="Country_Region",
            include=["Bolivia"]
        ),
        CompareOp(
            id="n29",
            meta=OpsMeta(nodeId="n29", inputs=["n2", "n28"], sentenceIndex=3),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n9",
            which="max"
        ),
        # limitation
        CountOp(
            id="n30",
            meta=OpsMeta(nodeId="n30", inputs=["n7", "n9", "n11", "n13", "n15", "n17", "n19", "n21", "n23", "n25", "n27", "n29"], sentenceIndex=3),
            field="Country_Region"
        )
    ],
    "ops4":[
        FilterOp(
            id="31",
            meta=OpsMeta(nodeId="n31", inputs=[], sentenceIndex=4),
            field="Country_Region",
            include=["Mexico", "Central America & Caribbean", "Bolivia", "Argentina", "Brazil", "Peru"]
        ),
        CountOp(
            id="n32",
            meta=OpsMeta(nodeId="n32", inputs=[], sentenceIndex=4),
            field="Country_Region"
        )
    ]
}


spec_4ldjaoujpydpkbu5 = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Inhabitants in millions",
            by="Gender",
            groupA="Male",
            groupB="Female"
        )
    ],
    "ops2": [
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Inhabitants in millions",
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=3),
            field="Inhabitants in millions",
            operator=">",
            value="ref:n2"
        )
    ],
    "ops4":[
        CountOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=4),
            field="Year"
        )
    ]
}


spec_0k75gqf8ckjikdym = {
    "ops":[
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Average age at marriage",
            by="Gender",
            groupA="Male",
            groupB="Female"
        ),
    ],
    "ops2":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Average age at marriage",
            which="min"
        )
    ],
    "ops3":[

    ]
}


spec_1p4nnba4568wza9n = {
    "ops": [
        CompareOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Percentage",
            targetA="Good",
            targetB="Bad",
            which="max"
        )
    ],
    "ops2":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n1", inputs=["n1"], sentenceIndex=1),
            field="Year",
            include=["2007", "2008"]
        )
    ],
    "ops3":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n1", inputs=["n1"], sentenceIndex=1),
            field="Opinion",
            include=["2009", "2010"]
        )
    ],
    "ops4":[
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=3),
            field="Year",
            operator="between",
            include=["2011", "2017"]
        ),
    ],
    "ops5":[
        
    ],
    "ops6":[
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=3),
            field="Year",
            operator="between",
            include=["2008", "2009"]
        ),
    ],
    "ops7":[
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=3),
            field="Year",
            operator="between",
            include=["2010", "2011"]
        )
    ],
    "ops8":[

    ],
    "ops9":[

    ],
    "ops10":[
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=10),
            field="Year",
            include=["2009", "2011"]
        )
    ],
    "ops11":[
        CountOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n6"], sentenceIndex=11),
            field="Year"
        )
    ]
}


spec_0gzowodb2py0d1s9 = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Revenue_Million_USD",
            by="Country_Region",
            groupA="Thailand",
            groupB="Philippines",
            signed=True
        )
    ],
    "ops2":[
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Revenue_Million_USD",
            operator=">",
            value=0
        )
    ],
    "ops3":[
        CountOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Year"
        )
    ]
}


spec_0nmj7sdej4cipma7 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2019"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2020"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Segment",
            include=["North America"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=1),
            field="Segment",
            include=["International"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1"], sentenceIndex=1),
            field="Segment",
            include=["Retail"]
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n2"], sentenceIndex=1),
            field="Segment",
            include=["North America"]
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n2"], sentenceIndex=1),
            field="Segment",
            include=["International"]
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n2"], sentenceIndex=1),
            field="Segment",
            include=["Retail"]
        )
    ],
    "ops2": [
        DiffOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n3", "n6"], sentenceIndex=1),
            targetA="ref:n3",
            targetB="ref:n6"
        ),
        DiffOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n4", "n7"], sentenceIndex=1),
            targetA="ref:n3",
            targetB="ref:n6"
        ),
        DiffOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n5", "n8"], sentenceIndex=1),
            targetA="ref:n3",
            targetB="ref:n6"
        ),
    ],

    "ops3": [
        FindExtremumOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n9", "n10", "n11"], sentenceIndex=1),
            field="Net sales in million US dollars"
        )
    ]
}


spec_0i9bxppwocx0tyop = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include= ["2008", "2009", "2010", "2011"]
        )
    ],
    "ops2": [
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Number of employees"
        ),
        ScaleOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            target="ref:n2",
            factor=1/4
        )
    ]
}


spec_0lua5jsw92d3enb4 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="2019"
        )        
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Share of respondents",
            operator="<",
            value=0.03
        )
    ],
    "ops3": [
        CountOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            field="Diet Type"
        )
    ]
}


spec_0iv07908ph6y6ifj = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Date",
            include=["Mar '16", "Mar '17", "Mar '18", "Mar '19"]
        )
    ],
    "ops2": [
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Active users in millions"
        ),
        ScaleOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            target="ref:n2",
            factor=1/4
        )
    ]
}


spec_1jabqwjz9pmd7qwz = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
        )
    ],
    "ops2": [
        SortOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            order="asc"
        )
    ],
    "ops3": [
        NthOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
            field="Number of facilities",
            order="asc",
            n=5
        ),
        NthOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=3),
            field="Number of facilities",
            order="asc",
            n=6
        ),
        AverageOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3", "n4"], sentenceIndex=3),
            field="Number of facilities"
        )
    ]
}


spec_1sf5c8wqw1192q6b = {
    "ops": [
        SumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Growth rate of HICP (%)"
        ),
        ScaleOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            target="ref:n1",
            factor=1/12
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Growth rate of HICP (%)",
            operator="<",
            value="ref:n1"
        )
    ],
    "ops3": [
        CountOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Month"
        )
    ]
}


spec_1vh62ks9wweck6m2 = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Level_of_Stress",
            by="Gender",
            groupA="Women",
            groupB="Men"
        )
    ],
    "ops2": [
        
    ],
    "ops3":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=3),
            field="Level_of_Stress",
            which="min"
        )
    ]
}


spec_0jbrb1dcbliiampz = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2011", "2012", "2013", "2014"]
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Investments in Billion Euros",
            operator=">",
            value=22
        )
    ],
    "ops3": [
        CountOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Year"
        )
    ]
}


spec_0ufvwi9xv37e597q = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Revenue_Million_Euros",
            by="Revenue_Type",
            groupA="Matchday",
            groupB="Commercial"
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Revenue_Million_Euros",
            which="max"
        )
    ]
}


spec_0oinwvo88bvvs25b = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Gender",
            group="Women"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Share of women and men",
            which="max"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Gender",
            group="Men"
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=1),
            field="Share of women and men",
            which="max"
        )
    ], 
    "ops3":[

    ],
    "ops4":[

    ],
    "ops5":[
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3", "n4"], sentenceIndex=2),
            field="Share of women and men",
            targetA="ref:n3",
            targetB="ref:n4"
        )
    ]
}



spec_1vni31fp2ii7wz68 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Month",
            include=["Aug '20", "Dec '20", "Jul '20", "Jun '20", "May '20", "Nov '20", "Oct '20", "Sep '20"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Month",
            include=["Feb '21", "Mar '21", "Apr '21", "May '21", "Jan '21"]
        )
    ],
    "ops2": [
        NthOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Month",
            order="asc",
            n=1
        ),
        NthOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=2),
            field="Month",
            order="asc",
            n=1
        ),
         NthOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1"], sentenceIndex=2),
            field="Month",
            order="desc",
            n=1
        ),
        NthOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n2"], sentenceIndex=2),
            field="Month",
            order="desc",
            n=1
        ),
    ],
    "ops3": [
        DiffOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n3", "n5"], sentenceIndex=3),
            field="Number in millions",
            targetA="ref:n5",
            targetB="ref:n3"
        ),
        DiffOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n4", "n6"], sentenceIndex=3),
            field="Number in millions",
            targetA="ref:n6",
            targetB="ref:n4"
        ),
    ],
    "ops4":[

    ]
}

spec_20gpvz4ylu4olrm7 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2000", "2004", "2008", "2012"]
        )
    ],
    "ops2": [
        PairDiffOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Percentage",
            by="Gender",
            groupA="Women",
            groupB="Men"
        )
    ],
    "ops3": [
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            field="Percentage"
        ),
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            target="ref:n3",
            factor=1/4
        )
    ]
}

spec_0k7bm9iqewnrzj47 = {
    "ops": [
        NthOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Production in million liters",
            order="desc",
            n=1
        ),
        NthOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Production in million liters",
            order="desc",
            n=2
        ),
        NthOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Production in million liters",
            order="desc",
            n=3
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1", "n2", "n3"], sentenceIndex=1),
            field="Production in million liters",
        )
    ],
    "ops2": [
        NthOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=1),
            field="Production in million liters",
            order="asc",
            n=1
        ),
        NthOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=1),
            field="Production in million liters",
            order="asc",
            n=2
        ),
        NthOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=1),
            field="Production in million liters",
            order="asc",
            n=3
        ),
        SumOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n5", "n6", "n7"], sentenceIndex=1),
            field="Production in million liters",
        ),
        ScaleOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n8"], sentenceIndex=3),
            field="Production in million liters",
            target="ref:n8",
            factor=2
        )
    ],
    "ops3": [
        DiffOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n4", "n9"], sentenceIndex=3),
            field="Production in million liters",
            targetA="ref:n4",
            targetB="ref:n9"
        )
    ]
}


spec_0vfqjaxeiv96ww7g = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=2),
            group=["Almost all of the time"]
        ),
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Race",
            include=["White"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Race",
            include=["Black"]
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=2),
            field="Percentage"
        ),
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2"], sentenceIndex=2),
            field="Percentage"
        )
    ],
    "ops3": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4", "n5"], sentenceIndex=3),
            field="Percentage",
            targetA="ref:n4",
            targetB="ref:n5"
        )
    ]
}

spec_0opt5fjw2xphdgp2 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Frequency",
            include=["Occasionally (less than once a month)"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Race/Ethnicity",
            include=["White"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Race/Ethnicity",
            include = ["Hispanic"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=1),
            field="Race/Ethnicity",
            include = ["African–American"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1"], sentenceIndex=1),
            field="Race/Ethnicity",
            include = ["Other"]
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=1),
            field="Frequency",
            include=["Infrequently (once a year or less)"]
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n6"], sentenceIndex=1),
            field="Race/Ethnicity",
            include=["White"]
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n6"], sentenceIndex=1),
            field="Race/Ethnicity",
            include = ["Hispanic"]
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n6"], sentenceIndex=1),
            field="Race/Ethnicity",
            include = ["African–American"]
        ),        
        FilterOp(
            id="n10",
            meta=OpsMeta(nodeId="n13", inputs=["n5"], sentenceIndex=1),
            field="Race/Ethnicity",
            include = ["Other"]
        ),
        SumOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n2", "n7"], sentenceIndex=1),
            field="Share of respondents"
        ),
        SumOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n3", "n8"], sentenceIndex=1),
            field="Share of respondents"
        ),
        SumOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=["n4", "n9"], sentenceIndex=1),
            field="Share of respondents"
        ),
        SumOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n12", "n10"], sentenceIndex=1),
            field="Share of respondents"
        )
    ],
    "ops2": [
        
    ],
    "ops3": [
        
    ],
    "ops4":[

    ],
    "ops5":[

    ],
    "ops6":[
        FindExtremumOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=["n11", "n12", "n13", "n14"], sentenceIndex=3),
            field="Share of respondents",
            which="max"
        )
    ],
    "ops7":[

    ],
    "ops8":[

    ],
    "ops9":[

    ]
}


spec_25gpdzxh8nu0c0vf = {
    "ops": [
        SumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Number_of_Fatalities"
        ),
        ScaleOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            target="ref:n1",
            factor=1/21
        ),
        
    ],
    "ops2": [
        NthOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Number_of_Fatalities",
            order="asc",
            n=10
        )
    ],
    "ops3": [
        CompareOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=3),
            field="Number_of_Fatalities",
            targetA="ref:n1",
            targetB="ref:n2",
            which="max"
        )
    ]
}


spec_20qa83ih1gn6toqt = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Has a great impact",
            by="Metric",
            groupA="Price",
            groupB="Convenience"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Has a great impact",
            include=["2012"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Has a great impact",
            include=["2013"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=1),
            field="Has a great impact",
            include=["2014"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1"], sentenceIndex=1),
            field="Has a great impact",
            include=["2015"]
        ),
        
    ],
    "ops3": [
        FindExtremumOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1"], sentenceIndex=3),
            field="Has a great impact",
            which="min"
        )
    ]
}


spec_0baf5ch9y4z8914p = {
    "ops": [
        SortOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Monetary policy rate (%)",
            order="asc"
        ),
        
    ],
    "ops2": [
        NthOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Monetary policy rate (%)",
            order="asc",
            n=1
        ),
        NthOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Monetary policy rate (%)",
            order="asc",
            n=2
        ),
        NthOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=1),
            field="Monetary policy rate (%)",
            order="asc",
            n=3
        )
    ],
    "ops3":[
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n3", "n4"], sentenceIndex=2),
            field="Monetary policy rate (%)",
        ),
        ScaleOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=2),
            field="Monetary policy rate (%)",
            target="ref:n5",
            factor=1/3
        )
    ]
}


spec_01h0jkno5l7jola8 = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            by="Gender",
            groupA="Men",
            groupB="Women"
        )
    ],
    "ops2": [
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Share of respondents"
        )
    ]
}


spec_0cjk67q39ee6dhzj = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Percentage of people negative on China",
            by="Party",
            groupA="Republicans",
            groupB="Democats"
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Year",
            which="max"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Year",
            which="min"
        )
    ],
    "ops3": [
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=4),
            field="Percentage of people negative on China",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
    ],
    "ops4": [],
    "ops5": [],
    "ops6": [],
    "ops7": [],
    "ops8": [],
    "ops9": [],
    "ops10": [],
    "ops11": [],
    "ops12": [],
    "ops13": [],
    "ops14": [],
    "ops15": [],
    "ops16": [],
    "ops17": [],
    "ops18": [],
    "ops19": [],
}


spec_01mksjs373fhcl4q = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Average length of lease in years",
            by="Year",
            groupA="mid-2013",
            groupB="2003"
        )
    ],
    "ops2": [
        
    ],
    "ops3":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Average length of lease in years",
            which="max"
        )
    ]
}


spec_04xwv56n37ybj8zr = {
    "ops":[

    ],
    "ops2": [
        SortOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Index_Score",
            order="desc"
        )
    ],
    "ops2": [
        NthOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Index_Score",
            n=3
        ),
        NthOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Index_Score",
            n=5
        )
    ],
    "ops3":[
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n3", inputs=["n2", "n3"], sentenceIndex=3),
            field="Index_Score",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ]
}


spec_0cymcilknp8krjwz = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Average Price (USD)",
            operator=">",
            value="4.0"
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Average Price (USD)"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Average Price (USD)",
            operator="<",
            value="2.5"
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Average Price (USD)"
        )
    ],
    "ops3": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Average Price (USD)",
            targetA="ref:n4",
            targetB="ref:n2"
        )
    ]
}


spec_0abj8blv663ussbr = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2010"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2020"]
        )
    ],
    "ops2": [
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=2),
            field="Market size in billion US dollars",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ]
}


spec_0cad2xfrwdgvo9zk = {
    "ops":[

    ],
    "ops2": [
        SortOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Number of fatalities",
            order="asc"
        ),
        NthOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Number of fatalities",
            n=6
        )
    ],
    "ops3": [
        NthOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Number of fatalities",
            n=6
        ),
        NthOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Number of fatalities",
            n=5
        ),
        NthOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=3),
            field="Number of fatalities",
            n=7
        )
    ],
    "ops4": [
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n3", "n4"], sentenceIndex=4),
            field="Number of fatalities"
        )
    ]
}


spec_0gr1c2jcthc8h9f6 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Risk index score",
            operator="between",
            value=["6.2", "5.8"]
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Risk index score",
            operator="<",
            value="4.8"
        )
    ],
    "ops3": [
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=3),
            field="Risk index score",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ]
}


spec_001dao0mq0pplbzj = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Revenue_Million_USD",
            by="Revenue_Type",
            groupA="Commercial",
            groupB="Matchday"
        )
    ],
    "ops2": [
        
    ],
    "ops3": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Revenue_Million_USD",
            which="max"
        )
    ]
}


spec_0a5npu4o61dz4r5f = {
    "ops": [
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Damage (in billion US dollars)",
            which="max"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Damage (in billion US dollars)",
            which="min"
        )
    ],
    "ops2": [
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=2),
            field="Damage (in billion US dollars)",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ]
}


spec_07lo3vvwztz32ifq = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Net_Sales_Percentage",
            group="2009"
        ),
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Net_Sales_Percentage",
            group="2010"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Net_Sales_Percentage",
            which="max",
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=1),
            field="Net_Sales_Percentage",
            which="min",
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3", "n4"], sentenceIndex=1),
            targetA="ref:n3",
            targetB="ref:n4"
        )
    ],
    "ops2":[],
    "ops3": [],
    "ops4":[
        FindExtremumOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=4),
            field="Net_Sales_Percentage",
            which="max"
        ),
        FindExtremumOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n5"], sentenceIndex=4),
            field="Net_Sales_Percentage",
            which="min"
        )
    ],
    "ops5": [
        SumOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n6", "n7"], sentenceIndex=4),
            field="Net_Sales_Percentage"
        )
    ],
    "ops6":[],
    "ops7":[],
    "ops8":[],
    "ops9":[],
    "ops10":[]
}


spec_075i5mfewy2uvwej = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Services"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Year",
            include=["2010"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Year",
            include=["2020"]
        )
    ],
    "ops2": [
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n3"], sentenceIndex=2),
            field="Share_of_Total_Employment",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ]
}


spec_08x3crju85yix5ab = {
    "ops":[],
    "ops2": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=2),
            field="CPI_Score",
            operator="<",
            value=80
        )
    ],
    "ops3": [
        CountOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=3),
            field="Year",
        ),
        
    ]
}


spec_004fhteah0l9kud2 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Revenue_Million_Euros",
            group="Commercial"
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Revenue_Million_Euros"
        ),
        ScaleOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            target="ref:n2",
            factor=1/6
        )
    ],
    "ops2": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Revenue_Million_Euros",
            group="Matchday"
        ),
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            field="Revenue_Million_Euros"
        ),
        ScaleOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=2),
            target="ref:n5",
            factor=1/6
        )
    ],
    "ops3": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3", "n6"], sentenceIndex=3),
            field="Revenue_Million_Euros",
            targetA="ref:n3",
            targetB="ref:n6"
        )
    ]
}


spec_0bunvsqd54e3qahz = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Life expectancy at birth in years",
            group="female"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Year",
            include=["2010"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Life expectancy at birth in years",
            group="male"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Year",
            include=["2016"]
        ),
    ],
    "ops2": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=2),
            field="Life expectancy at birth in years",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}


spec_0bgcjlbz7nv5vnjc = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share (%)",
            by="Age Group",
            groupA="5–10 years",
            groupB="11–15 years"
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Share (%)",
            which="max"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Share (%)",
            which="max",
            rank=2
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=1),
            field="Share (%)",
            which="max",
            rank=3
        )
    ],
    "ops3": [
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n3", "n4"], sentenceIndex=3),
            field="Share (%)",
        ),
        ScaleOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=3),
            target="ref:n5",
            factor=1/3
        )
    ]
}


spec_08iur64i01boakg5 = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Percentage of 25 to 29 year olds",
            by="Gender",
            groupA="Male",
            groupB="Female"
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Percentage of 25 to 29 year olds",
            which="max"
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Year",
            include=["2017"]
        )
    ]
}


spec_05qg5ubxklojfze7 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Major problem"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            group="Minor problem"
        )
    ],
    "ops2": [
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Share_of_Respondents"
        )
    ],
    "ops3":[
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Share_of_Respondents",
            which="max"
        )
    ]
}


spec_0b9o2vahkw2a1bxy = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share_of_Respondents",
            group="No"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Share_of_Respondents",
            which="max"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Share_of_Respondents",
            group="Yes"
        ),
        SortOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Share_of_Respondents",
        )
    ],
    "ops3": [
        FindExtremumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=3),
            field="Share_of_Respondents",
            which="max"
        ),
        NthOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n3"], sentenceIndex=3),
            field="Share_of_Respondents",
            order="desc",
            n=3
        ),
        DiffOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n5", "n6"], sentenceIndex=3),
            field="Share_of_Respondents"
        )
    ],
    "ops4": [
        DiffOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n2", "n5"], sentenceIndex=4),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n5"
        ),
    ]
}


spec_0v0l4wdbx7orkqz1 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Age group",
            include=["15–19", "20–24", "25–29"]
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Suicides per 100,000 population",
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Age group",
            include=["70–74", "75–79", "80–84", "85–89", "90+"]
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Suicides per 100,000 population",
        )
    ],
    "ops3":[
        CompareOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=2),
            field="Suicides per 100,000 population",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}


spec_14jud3ymyoonba4e = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Global Performance Nutrition"
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Revenue_Million_Euros",
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            group="Global Nutritionals"
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Revenue_Million_Euros",
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=1),
            group="Joint Ventures & Associates"
        ),
        SumOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=1),
            field="Revenue_Million_Euros",
        ),
        
    ],
    "ops2": [
        FindExtremumOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n2", "n4", "n6"], sentenceIndex=1),
            field="Revenue_Million_Euros",
            which="max"
        )
    ]
}


spec_0vw6ydim9cff8ji6 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Industry Sector",
            include=["Construction"]
        )
    ],
    "ops2": [
        
    ],
    "ops3":[
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Share of SMEs",
            which="max"
        )
    ]
}


spec_5lhrulhnl0io2r81 = {
    "ops":[],
    "ops2": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Producer Price Index (100=2009)",
            operator="<",
            value=210
        ),
        
    ],
    "ops3": [
        CountOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Month/Year"
        )
    ]
}


spec_2hjkdo5w242alvjd = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2006", "2007", "2008", "2009", "2010", "2011"]
        ),
        CountOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Year"
        )
    ],
    "ops2": [
        PairDiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Percentage_of_Respondents",
            by="Opinion",
            groupA="Dissatisfied",
            groupB="Satisfied",
            signed=True
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Percentage_of_Respondents",
            operator="<",
            value=0
        )
    ],
    "ops3": [
        CountOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=3),
            field="Year",
        )
    ],
    "ops4": [
        CompareOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n2", "n5"], sentenceIndex=4),
            field="Year",
            targetA="ref:n2",
            targetB="ref:n5"
        )
        
    ]
}


spec_0vmvmj77j3p6vcy7 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2010", "2011", "2012", "2013", "2014", "2015"]
        )
    ],
    "ops2":[
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Net income in USD",
        )
    ]
}


spec_174uq759pluu079w = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2017"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Year",
            include=["2018"]
        ),
        
    ],
    "ops2": [
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Shipments_Million_Units",
            which="max"
        )
    ],
    "ops3": [
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=3),
            field="Shipments_Million_Units",
            which="max"
        )
    ],
    "ops4":[
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3", "n4"], sentenceIndex=1),
            field="Shipments_Million_Units",
        )
    ]
}

# 확인
spec_0w5jptak9peti0mj = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2015"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2016"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2017"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2018"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2019"]
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2020"]
        ),
    ],
    "ops2": [
        FindExtremumOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n1"], sentenceIndex=2),
            field="Annual revenue in million USD",
            which="min"
        ),
        FindExtremumOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n2"], sentenceIndex=2),
            field="Annual revenue in million USD",
            which="min"
        ),
        FindExtremumOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n3"], sentenceIndex=2),
            field="Annual revenue in million USD",
            which="min"
        ),
        FindExtremumOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n4"], sentenceIndex=2),
            field="Annual revenue in million USD",
            which="min"
        ),
        FindExtremumOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n1"], sentenceIndex=2),
            field="Annual revenue in million USD",
            which="min"
        )
    ],
    "ops3": [
        FilterOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=[], sentenceIndex=3),
            field="Year",
            include=["2015", "2016", "2017", "2018", "2019", "2020"]
        )
    ],
    "ops4":[
        CountOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=[], sentenceIndex=4),
            field="Year"
        )
    ]
}


spec_5po479f2ju9lqv16 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2011", "2012", "2013", "2014", "2015", "2016", "2017"]
        )
    ],
    "ops2": [
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Inhabitants in billions",
        )
    ]
}


spec_2kmpy10btl65kr2j = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Opinion_Type",
            group="Favorable view of U.S."
        )
        
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Year",
            include=["2015", "2016", "2017"]
        )
    ],
    "ops3": [
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Percentage_of_Respondents",
        ),
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            target="ref:n3",
            factor=1/3
        )
    ]
}


spec_0vqxnzu0mpbz12ch = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2018"]
        ),
         FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2019"]
        ),
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=1),
            field="Year",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ],
    "ops2": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2023"]
        ),
         FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2025"]
        ),
        DiffOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n4", "n5"], sentenceIndex=2),
            field="Year",
            targetA="ref:n4",
            targetB="ref:n5"
        )
    ],
    "ops3": [
        CompareOp(
            id="n7",
            meta=OpsMeta(nodeId="n6", inputs=["n3", "n6"], sentenceIndex=3),
            field="Share of population with a smartphone",
            targetA="ref:n3",
            targetB="ref:n6",
            which="max"
        )
    ]
}


spec_19xwo5oscmgpcdyl = {
    "ops": [

    ],
    "ops2": [

    ],
    "ops3": [

    ]
}


spec_0wgqpso2vnilpym6 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Region",
            include=["Alaska"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Year",
            group="2000"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Year",
            group="2020"
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Year",
        )
    ],
    "ops2": [
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=1),
            field="Region",
            include=["Total"]
        ),
        DiffOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1"], sentenceIndex=1),
            field="Production in million barrels per day",
        )
    ],
    "ops3": [
        CompareOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n4", "n6"], sentenceIndex=1),
            field="Production in million barrels per day",
            targetA="ref:n4",
            targetB="ref:n6"
        )
    ]
}


# 다시
spec_651x1l1swysyy6vp = {
    "ops": [
        
    ],
    "ops2": [
        SortOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=2),
            field="Share of respondents who are worried",
            order="desc"
        )
    ],
    "ops3": [
        NthOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Share of respondents who are worried",
            order="desc",
            n=5
        )
    ],
    "ops4":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            include=["Apr 28 to 29, 2020", "Oct 29, 2020"]
        )
    ],
    "ops5":[],
    "ops6":[],
    "ops7":[],
    "ops8":[],
    "ops9":[
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=9),
            include=["Apr 28 to 29, 2020"]
        )
    ]
}


spec_2s65jcap9pn289qx = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2016", "2017", "2018", "2019", "2020"]
        ),
    ],
    "ops2": [
        PairDiffOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Population_Million_Inhabitants",
            by="Gender",
            groupA="Female",
            groupB="Male"
        )
    ],
    "ops3": [
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Population_Million_Inhabitants",
        )
    ]
}


spec_0vvz9mdgdiazke5o = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2012", "2013", "2014", "2015"]
        ),
    ],
    "ops2": [
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Gross payment volume in billion USD",
        )
    ],
    "ops3":[
        ScaleOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            target="ref:n2",
            factor=1/4
        )
    ]
}


spec_19msoowya2szdynd = {
    "ops": [
    ],
    "ops2": [

    ],
    "ops3": [

    ]
}


spec_0xc7sx6ll8fl5rgh = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Percentage of votes",
            by="Candidate",
            groupA="Hillary Clinton",
            groupB="Bernie Sanders",
            signed=True
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Percentage of votes",
            operator=">",
            value=0
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            group="Hillary Clinton"
        )
    ],
    "ops3":[
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            field="Percentage of votes"
        )
    ]
}


spec_66va2s35es5t86l3 = {
    "ops": [
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="In millions"
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="In millions",
            which="max"
        )
    ],
    "ops3": [
        RetrieveValueOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Year",
            target=2010
        )
    ]
}


spec_3tc31k5k2o6wmvyp = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Date",
            include=["Jul 14"]
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Percent_Do_Not_Want_Reelected"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Date",
            include=["Jun 02"]
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Percent_Do_Not_Want_Reelected"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=1),
            field="Date",
            include=["Jun 06"]
        ),
        SumOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=1),
            field="Percent_Do_Not_Want_Reelected"
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=1),
            field="Date",
            include=["Jun 10"]
        ),
        SumOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n7"], sentenceIndex=1),
            field="Percent_Do_Not_Want_Reelected"
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[], sentenceIndex=1),
            field="Date",
            include=["Mar 98"]
        ),
        SumOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n9"], sentenceIndex=1),
            field="Percent_Do_Not_Want_Reelected"
        ),
        FilterOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=[], sentenceIndex=1),
            field="Date",
            include=["Oct 94"]
        ),
        SumOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n11"], sentenceIndex=1),
            field="Percent_Do_Not_Want_Reelected"
        ),
    ],
    "ops2": [
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=["n2", "n4", "n6", "n8", "n10", "n12"], sentenceIndex=2),
            field="Percent_Do_Not_Want_Reelected",
            operator="<",
            value=70
        )
    ],
    "ops3": [
        CountOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Date"
        )
    ]
}


spec_1h4rj9i2jtzq589y = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="EU 5-country median"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Favorable_View_Percentage",
            operator="between",
            value=["51", "61"]
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Year",
            include=["2012", "2013", "2014", "2015"]
        )
    ],
    "ops4": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=4),
            field="Year",
            include=["2012"]
        )
    ]
}


spec_0gf8ugj84bs1ko2k = {
    "ops": [
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Revenue_Million_USD",
            which="max"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2022"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            group="Data Centers"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=2),
            group="Cloud"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2"], sentenceIndex=2),
            group="BPO"
        )
    ],
    "ops3": [
        AverageOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n2"], sentenceIndex=3),
            field="Revenue_Million_USD"
        )
    ]
}


spec_14jt6jor7iknkjkl = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group=["Favorable view of US"]
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Percentage",
            which="min"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Year",
            include=["2009"]
        )        
    ],
    "ops3": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=3),
            group="Confidence in US president"
        )
    ],
    "ops4": [
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=4),
            field="Percentage"
        )
    ]
}


spec_16aphfabldrpgcmd = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Boys"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Average weight in metric grams",
            operator=">",
            value=3670
        ),
        CountOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            field="Year"
        )
    ],
    "ops2": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            group="Girls"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            field="Average weight in metric grams",
            operator=">",
            value=3550
        ),
        CountOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=2),
            field="Year"
        )
    ],
    "ops3": [
        SumOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n3", "n6"], sentenceIndex=3),
            field="Year"
        )
    ]
}


spec_0dglnk2wbf5ll15t = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Poor"
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Share of Respondents (%)"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            group="Good"
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Share of Respondents (%)"
        )
    ],
    "ops3": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Share of Respondents (%)",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}


spec_10gtgmmgh599jnr7 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            include=["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008"]
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Percentage_of_Population",
            which="min"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Percentage_of_Population",
            which="max",
            rank=2
        )
    ],
    "ops3": [
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=3),
            field="Percentage_of_Population",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ],
    "ops4": [],
    "ops5": [],
    "ops6": [],
    "ops7": []
}

# 확인
spec_0ix8hz9qvakto18g = {
    "ops": [
        SortOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Ease of doing business score"
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Ease of doing business score",
            which="max"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Ease of doing business score",
            which="max",
            rank=2
        )
    ],
    "ops3": [
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=3),
            field="Ease of doing business score",
            which="min"
        ),
        FindExtremumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1"], sentenceIndex=3),
            field="Ease of doing business score",
            which="min",
            rank=2
        )
    ],
    "ops4": [
        RetrieveValueOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1"], sentenceIndex=4),
            field="Year",
            target=2019
        ),
        RetrieveValueOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n1"], sentenceIndex=4),
            field="Year",
            target=2016
        ),
        SumOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n6", "n7"], sentenceIndex=4),
            field="Year",
        )
    ]
}


spec_0egdxqun1m2n9k4z = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            include=["2006", "2007", "2008", "2009", "2010", "2011"]
        )
    ],
    "ops2": [
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Revenue multiple",
        ),
        ScaleOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            target="ref:n2",
            factor=1/6
        )
    ]
}


spec_0aj7na7tkqb7iomu = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Tablets"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Year",
            include=["2017"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            group="Mobile PCs"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            field="Year",
            include=["2022"]
        )
    ],
    "ops2": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=2),
            field="Installed_Base_Millions",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}


spec_0gvrmm8qbn6o1vya = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Average ticket price in US dollars",
            operator="<=",
            value=60
        ),
    ],
    "ops2": [
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Average ticket price in US dollars",
        ),
        ScaleOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            target="ref:n2",
            factor=1/6
        )
    ]
}


spec_0egzejn5mejtnfdm = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Scotland"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="SharePercentage",
            which="max"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            group="England & Wales"
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="SharePercentage",
            which="min"
        )
    ],
    "ops3": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=2),
            field="SharePercentage",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}

# 확인
spec_0roec4s0drcyiuz4 = {
    "ops": [
        
    ],
    "ops2": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Quarter",
            include=["Q1 2019", "Q2 2020"]
        )
    ],
    "ops3": [

    ]
}


spec_0eq4w2wsl864mhcj = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Sales volume in million units",
            operator=">=",
            value=60
        )
    ],
    "ops2": [
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Sales volume in million units",
        ),
        ScaleOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            target="ref:n2",
            factor=1/3
        )
    ]
}


spec_0g0xma0b0k29lk5j = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share_of_Total_Population",
            by="Age_Group",
            groupA="15–64 years",
            groupB="65 years and older"
        )
    ],
    "ops2": [
        SortOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Share_of_Total_Population",
            order="desc"
        )
    ],
    "ops3": [
        NthOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n2"], sentenceIndex=3),
            field="Share_of_Total_Population",
            order="desc",
            n=2
        )
    ]
}


spec_0fhm43s0j7glca29 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="2018"
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Revenue in billion US dollars"
        ),
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Revenue in billion US dollars"
        )
    ],
    "ops2": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            group="2020"
        ),
        FindExtremumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            field="Revenue in billion US dollars",
            which="max"
        )
    ],
    "ops3": [
        CompareOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n3", "n5"], sentenceIndex=3),
            field="Revenue in billion US dollars",
            targetA="ref:n3",
            targetB="ref:n5",
            which="max"
        )
    ],
    "ops4": [
        RetrieveValueOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n6"], sentenceIndex=4),
            field="Year"
        )
    ]
}


spec_0gacqohbzj07n25s = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Country",
            include=["Russia", "Germany", "France", "Italy"]
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Number of procedures"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Country",
            include=["India", "Turkey", "Japan"]
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Number of procedures"
        )
    ],
    "ops3": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Number of procedures",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}


spec_1c80b6i7wdu3m1ir = {
    "ops": [
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year on yaer percentage change (%)"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Year on yaer percentage change (%)",
            operator="<",
            value=0
        ),
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2004", "2005", "2006", "2007", "2008"]
        )
    ],
    "ops3": [
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            field="Year on yaer percentage change (%)"
        )
    ]
}


spec_1k8qhmg9rui7gtzh = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2010", "2011", "2012", "2013", "2014", "2015"]
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            group="Germany"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Favorable_View_Percentage",
            which="max"
        )
    ],
    "ops3": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=3),
            group="US"
        ),
        FindExtremumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=3),
            field="Favorable_View_Percentage",
            which="min"
        )
    ],
    "ops4": [
        DiffOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n3", "n5"], sentenceIndex=3),
            field="Favorable_View_Percentage",
            targetA="ref:n3",
            targetB="ref:n5"
        )
    ]
}


spec_0ihx2vzdsej883sq = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Female"
        )
    ],
    "ops2": [
        SortOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Share of employees",
            order="asc"
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            include=["Leadership"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=1),
            group="Male"
        )
    ],
    "ops4":[],
    "ops5":[],
    "ops6":[],
    "ops7":[]
}


spec_0fh0emp095qhq3ag = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            include=["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Number of victims",
            which="max"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Number of victims",
            which="min"
        )
    ],
    "ops3": [
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=3),
            field="Number of victims",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ]
}





spec_21fa7gb8l1ix6yfm = {
    "ops": [
        CompareOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share of respondents",
            targetA="ref:n1",
            targetB="ref:n2",
            which="max"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Gender",
            operator="==",
            value="Male"
        )
    ],
    "ops2":[
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            group="Female"
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Share of respondents"
        )
    ],
    "ops3":[
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1"], sentenceIndex=3),
            field="Gender",
            operator="==",
            value="Female"
        )
    ],
    "ops4":[
        AverageOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=4),
            field="Share of respondents"
        )
    ],
    "ops5":[
        DiffOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n3", "n6"], sentenceIndex=5),
            field="Share of respondents",
            targetA="ref:n6",
            targetB="ref:n3"
        )
    ]
}


spec_54gh54f24irr63pb = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["2018"]
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Number_of_States",
            which="max"
        )
    ]
}


spec_1p6uue3hxdxit3ey = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="30 to 44 years"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Response",
            include=["No"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"]),
            field="Response",
            include=["Yes"]
        ),
        CompareOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"]),
            field="Percentage of respondents",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ]
}



spec_1fngt6cb1d60a2ow = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Region/Entity",
            exclude=["Metro Total"]
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Number of employees"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"]),
            field="Number of employees",
            operator="<",
            value=50000
        )
    ]
}



spec_6rvtt4egfl5nmyue = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["2012", "2013", "2014", "2015", "2016", "2017"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            group="female"
        ),
        NthOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            field="Life expectancy at birth in years",
            order="desc",
            n=2
        ),
        RetrieveValueOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Year",
        )
        
    ]
}


spec_1suppecte0dm69gm = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Not at all"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Respondent Group",
            include=["Men", "Women"]
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            field="Percentage of respondents",
        ),
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Percentage of respondents",
            target="ref:n3",
            factor=1/2
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1"]),
            field="Percentage of respondents",
            include=["All adults"]
        ),
        CompareBoolOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n4", "n5"]),
            operator=">",
            targetA="ref:n4",
            targetB="ref:n5"
        )
    ]
}


spec_1e56qqj7moat9gqa = {
    "ops": [
        SumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Spending in billion US dollars"
        )
    ]
}



spec_6p4fnscalopvysnn = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Share of the population",
            operator=">",
            value=40
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Share of the population",
            which="max"
        )
    ]
}


spec_50y71e5i2n28gkbx = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group=["Sportswear", "Running"]
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Revenue_Million_USD"
        )
    ]
}


spec_75yz7pci1w1dif3g = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Share_of_Respondents",
            by="Crisp_Flavor",
            groupA="None of these",
            groupB="Cheese and onion"
        ),
        SortOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Share_of_Respondents",
            order="desc"
        )
    ]
}


spec_7extlfw651gqc5fk = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Large"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Percentage",
            which="max"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            group="Small"
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Percentage",
            which="min"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[]),
            field="Year",
            include=["2010"]
        ),
        DiffOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n2", "n4"]),
            field="Percentage",
            targetA="ref:n2",
            targetB="ref:n4"
        ),
        AverageOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[]),
            field="Percentage",
        ),
        CompareBoolOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n6", "n7"]),
            field="Percentage",
            operator="==",
            targetA="ref:n6",
            targetB="ref:n7"
        )
        
    ]
}



spec_6rqevjp16hadlyly = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Male"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Year",
            include=["2007/08"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            field="Year",
            include=["2011/12"]
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"]),
            field="Percentage of tests passed",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[]),
            group="Female"
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"]),
            field="Year",
            include=["2007/08"]
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n5"]),
            field="Year",
            include=["2011/12"]
        ),
        DiffOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n6", "n7"]),
            field="Percentage of tests passed",
            targetA="ref:n6",
            targetB="ref:n7"
        ),
        CompareBoolOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n4", "n8"]),
            field="Percentage of tests passed",
            operator="==",
            targetA="ref:n4",
            targetB="ref:n8"
        )
    ]
}



spec_1esx2fbduhqn7knk = {
    "ops": [
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Deaths",
            which="max"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Deaths",
            which="min"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"]),
            field="Deaths",
            exclude=["ref:n1", "ref:n2"]
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Deaths"
        )
    ]
}


spec_1epzpacytv3wx2i6 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["2010", "2011", "2012", "2013"]
        ),
        LagDiffOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Market size in million GBP",
            signed=True
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            field="Market size in million GBP",
            operator=">",
            value=0
        )
    ]
}


spec_1qm2z3ooawf339jz = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="East"
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Share of respondents"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            group="Scotland"
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Share of respondents"
        ),
        CompareOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[]),
            field="Share of respondents",
            which="max"
        )
    ]
}



spec_95yhyqjyeu4fohbj = {
    "ops": [
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Number of people in millions",
            which="max"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Number of people in millions",
            which="min"
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"]),
            field="Number of people in millions"
        ),
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Number of people in millions",
            target="ref:n3",
            factor=1/2
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[]),
            field="Year",
            include=["2010"]
        ),
        CompareBoolOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n4", "n5"]),
            field="Number of people in millions",
            operator=">",
            targetA="ref:n4",
            targetB="ref:n5"
        )
    ]
}


spec_62w3xg16iivw11et = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            group="Industry"
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            field="Share_of_GDP"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"]),
            group="Industry"
        ),
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"]),
            field="Share_of_GDP"
        ),
        CompareBoolOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n3", "n5"]),
            field="Share_of_GDP",
            operator="==",
            targetA="ref:n3",
            targetB="ref:n5"
        )
    ]
}


spec_95wcyze391ifhegp = {
    "ops": [
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Exchange rate in Singapore dollars",
            which="max"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Exchange rate in Singapore dollars",
            which="min"
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"]),
            field="Exchange rate in Singapore dollars"
        ),
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Exchange rate in Singapore dollars",
            target="ref:n3",
            factor=1/2
        )
    ]
}

spec_9douccar3m9ruah4 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["2017", "2018"]
        )
    ]
}


spec_9mlpjn6pddrbthj8 = {
    "ops": [
        NthOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Number of fatalities",
            order="asc",
            n=3
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Year",
            include=["2011", "2012"]
        ),
        CompareBoolOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"]),
            field="Number of fatalities",
            operator=">",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ]
}


spec_1x37jzohqd666qc0 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Don't know/no opinion"
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Percentage of respondents"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            group="Very unlikely"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Category",
            include=["Family"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3"]),
            field="Category",
            include=["Local community"]
        ),
        DiffOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n4", "n5"]),
            field="Percentage of respondents",
            targetA="ref:n4",
            targetB="ref:n5"
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[]),
            group="Somewhat unlikely"
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n7"]),
            field="Category",
            include=["Family"]
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n7"]),
            field="Category",
            include=["Local community"]
        ),
        DiffOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n8", "n9"]),
            field="Percentage of respondents",
            targetA="ref:n8",
            targetB="ref:n9"
        ),
        SumOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n6", "n10"]),
            field="Percentage of respondents",
        ),
        CompareBoolOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n2", "n10"]),
            operator="==",
            targetA="ref:n2",
            targetB="ref:n10"
        )
    ]
}


spec_1bv05pu9d8jnidty = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["2020", "2021", "2022", "2023", "2024", "2025"]
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="National debt in billion US dollars",
        )
    ]
}



spec_2mi8b2r0oalayl6g = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group=["Footjoy golf wear", "Titleist golf gear"]
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Revenue in million US dollars",
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            field="Revenue in million US dollars",
            which="max"
        )
    ]
}


spec_82aqt0k0jnbj3irf = {
    "ops": [
        NthOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Number of enterprises",
            order="asc",
            n=5
        )
    ]
}


spec_1jatwi94v2d8cr9u = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Digital market"
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Value in billion US dollars"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            group="Package market"
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Value in billion US dollars"
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"]),
            field="Value in billion US dollars",
            targetA="ref:n4",
            targetB="ref:n2"
        )
    ]
}


spec_2bhsybiilde28j87 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Very interested"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Share_of_Respondents",
            include=["White", "Hispanic", "Other"]
        ),
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            field="Share_of_Respondents",
        ),
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Share_of_Respondents",
            target="ref:n3",
            factor=100
        )
    ]
}


spec_1bywaj7stsb3060c = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Company",
            include=["Conad", "Selex", "Agorà", "MD", "Crai"]
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Market shares"
        )
    ]
}


spec_6ah60yba8o7rw0i9 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Yoghurt with additives"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Average_Price_Euros",
            which="max"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            group="Yoghurt without additives"
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Average_Price_Euros",
            which="min"
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"]),
            field="Average_Price_Euros",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}


spec_5p6g89v7l99aes05 = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Average_Payroll_Million_USD",
            by="Team_Group",
            groupA="All teams",
            groupB="Playoff teams"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Average_Payroll_Million_USD",
            which="max"
        )
    ]
}



spec_1ce802l2rdg98d7d = {
    "ops": [
        NthOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Share of respondents",
            n=3
        )
    ]
}


spec_1hokbw2gmzar9ye8 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="60 years and over"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            include=["Women"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            group="18 to 39 years"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            include=["Men"]
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"]),
            field="Percentage of adults",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}


spec_5wpw8detqynmqv1s = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Female"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Number_of_Victims",
            which="max"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            group="Male"
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Number_of_Victims",
            which="min"
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"]),
            field="Number_of_Victims",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}



spec_8e9wp443ff1i6snq = {
    "ops": [
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Immigration rate per thousand inhabitants"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Immigration rate per thousand inhabitants",
            which="max"
        )
    ]
}



spec_2n0g3tsz1rsz6fgr = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Industry"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Year",
            include=["2010", "2011", "2012", "2013", "2014"]
        ),
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            field="Share of total employment"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"]),
            include=["2011", "2012", "2013", "2014", "2015"]
        ),
        AverageOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"]),
            field="Share of total employment"
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1"]),
            include=["2012", "2013", "2014", "2015", "2016"]
        ),
        AverageOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n6"]),
            field="Share of total employment"
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n1"]),
            include=["2016", "2017", "2018", "2019", "2020"]
        ),
        AverageOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n8"]),
            field="Share of total employment"
        ),
        FindExtremumOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n3", "n5", "n7", "n9"]),
            field="Share of total employment",
            which="max"
        )
    ]
}



spec_8chfa8n079zpfigi = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="FIFA World Ranking position",
            operator="between",
            value=["20", "30"]
        ),
        CountOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Year"
        )
    ]
}



spec_1j7gx35h6i9mpi6j = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Much more important/A little more important"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Item",
            include=["Books"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"]),
            field="Item",
            include=["Beauty products"]
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"]),
            field="Share of respondents",
            targetA="ref:n2",
            targetB="ref:n3"
        )
        
    ]
}


spec_2yech0pea1xihind = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Platform",
            include=["Facebook", "Instagram"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            group="Several times a day"
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            field="Percentage"
        )
    ]
}



spec_64ue1v00wj8vg48e = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["1996", "1999", "2004", "2005", "2006", "2007", "2008", "2009"]
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Share of respondent"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            include=["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Share of respondent"
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"]),
            field="Share of total employment",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}



spec_1dm30xw1gpjo8ke5 = {
    "ops": [
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Share of GDP",
            which="max"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Share of GDP",
            which="min"
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"]),
            field="Share of total employment",
        ),
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            target="ref:n3",
            factor=1/2
        )
    ]
}


spec_8hiwwys6qkrbtapb = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["2002/03", "2003/04", "2004/05", "2005/06", "2006/07", "2007/08", "2008/09", "2009/10"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Year",
            include=["2010/11", "2011/12", "2012/13", "2013/14", "2014/15", "2015/16", "2016/17", "2017/18", "2018/19", "2019/20"]
        ),
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"]),
            field="Crime rate per 1,000 population"
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"]),
            field="Crime rate per 1,000 population"
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3", "n4"]),
            field="Crime rate per 1,000 population",
            targetA="ref:n3",
            targetB="ref:n4"
        )
    ]
}


spec_9u3xwiltv2hlcqq1 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Enterprises"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            group="Provider"
        ),
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"]),
            field="Share of respondents",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ]
}


spec_9u3xwiltv2hlcqq1 = {
    "ops": [
        FilterOp(
            include=["2007", "2011", "2012"]
        ),
        FilterOp(
            group="Democratic government"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            include=["2002", "2005"]
        )
    ]
}


spec_1hv85ef35tbvldiq = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Revenue in billion US dollars",
            operator="<",
            value=2.0
        ),
        CountOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Year"
        )
    ]
}


spec_au22oa0vjosoagxu = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="male"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Year",
            include=["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"]
        )
    ]
}


spec_albgfrf44bz6134k = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["2009"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Year",
            include=["2019"]
        ),
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"]),
            field="Inhabitants in millions",
            targetA="ref:n1",
            targetB="ref:n2"
        ),
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            target="ref:n3",
            factor=1/2
        ),
        LagDiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[]),
            field="Inhabitants in millions"
        ),
        CompareBoolOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[]),
            operator="==",
            field="Inhabitants in millions",
            targetA="ref:n3",
            targetB="ref:n4"
        )
    ]
}



spec_23bplnbw291p6nil = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Age_Group",
            include=["50 to 59"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            group="female"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"]),
            group="male"
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Median_Annual_Pay_GBP",
            targetA="ref:n2",
            targetB="ref:n2"
        )
    ]
}


spec_aoycx517slbw0ifa = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            include=["2015", "2016", "2017", "2018"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            group="Entertainment division"
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"]),
            field="Revenue in million euros"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"]),
            group="Enterprise division"
        ),
        SumOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"]),
            field="Revenue in million euros"
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"]),
            group="Healthcare division"
        ),
        SumOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n6"]),
            field="Revenue in million euros"
        ),
        CompareOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n3", "n5"]),
            which="max",
            targetA="ref:n3",
            targetB="ref:n5"
        ),
        CompareOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n7", "n8"]),
            which="max",
            targetA="ref:n7",
            targetB="ref:n8"
        )
    ]
}


spec_aqowly2mmavof3f1 = {
    "ops": [
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Unemployment rate",
            signed=True
        ),
        FilterOp(
            include=["1992", ""]
        )
    ]
}


spec_23zc8kuhnpespj98 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Boys"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Share_of_Respondents",
            which="max"
        )
    ]
}


spec_1hm06wtar7gh92c8 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            include=["2020"]
        ),
        ScaleOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            target="ref:n1",
            factor=100000
        )
    ]
}



spec_amn6abwhwmc7ksaz = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Quarter/Year",
            include=["Q1 '16", "Q2 '16", "Q3 '16",  "Q4 '16"]
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Price in US dollars per peak watt",
            which="max"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            field="Price in US dollars per peak watt",
            which="min"
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"]),
            field="Price in US dollars per peak watt",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[]),
            field="Quarter/Year",
            include=["Q1 '17", "Q2 '17", "Q3 '17", "Q4 '17"]
        ),
        FindExtremumOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"]),
            field="Price in US dollars per peak watt",
            which="max"
        ),
        FindExtremumOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n5"]),
            field="Price in US dollars per peak watt",
            which="min"
        ),
        DiffOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n6", "n7"]),
            field="Price in US dollars per peak watt",
            targetA="n6",
            targetB="n7"
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[]),
            field="Quarter/Year",
            include=["Q1 '18", "Q2 '18", "Q3 '18", "Q4 '18"]
        ),
        FindExtremumOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n9"]),
            field="Price in US dollars per peak watt",
            which="max"
        ),
        FindExtremumOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n9"]),
            field="Price in US dollars per peak watt",
            which="min"
        ),
        DiffOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n10", "n11"]),
            field="Price in US dollars per peak watt",
            targetA="n10",
            targetB="n11"
        ),
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=[]),
            field="Quarter/Year",
            include=["Q1 '19", "Q2 '19", "Q3 '19", "Q4 '19"]
        ),
        FindExtremumOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n13"]),
            field="Price in US dollars per peak watt",
            which="max"
        ),
        FindExtremumOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=["n13"]),
            field="Price in US dollars per peak watt",
            which="min"
        ),
        DiffOp(
            id="n16",
            meta=OpsMeta(nodeId="n16", inputs=["n14", "n15"]),
            field="Price in US dollars per peak watt",
            targetA="ref:n14",
            targetB="ref:n15"
        ),
        FilterOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=[]),
            field="Quarter/Year",
            include=["Q1 '20", "Q2 '20", "Q3 '20"]
        ),
        FindExtremumOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=["n17"]),
            field="Price in US dollars per peak watt",
            which="max"
        ),
        FindExtremumOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=["n17"]),
            field="Price in US dollars per peak watt",
            which="min"
        ),
        DiffOp(
            id="n20",
            meta=OpsMeta(nodeId="n19", inputs=["n18", "n19"]),
            field="Price in US dollars per peak watt",
            targetA="ref:n18",
            targetB="ref:n19"
        ),
        FindExtremumOp(
            id="n21",
            meta=OpsMeta(nodeId="n21", inputs=["n4", "n8", "n12", "n16", "n19"]),
            field="Price in US dollars per peak watt",
            which="max"
        )
    ]
}


spec_221xoyhy3yziwabm = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Satisfaction_Level",
            include=["Very satisfied", "Somewhat satisfied"]
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Share_of_Respondents"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            field="Satisfaction_Level",
            include=["Somewhat dissatisfied", "Very dissatisfied"]
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Share_of_Respondents"
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"]),
            field="Share_of_Respondents",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}



spec_25n4mzhv6y1p36dl = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Spend more"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Share_of_Respondents",
            which="min"
        )
    ]
}


spec_ay58pwlf97q0osw6 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="Commercial"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Revenue in million euros",
            which="max"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"]),
            field="Revenue in million euros",
            which="min"
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"]),
            field="Revenue in million euros",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[]),
            group="Matchday"
        ),
        FindExtremumOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"]),
            field="Revenue in million euros",
            which="max"
        ),
        FindExtremumOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n5"]),
            field="Revenue in million euros",
            which="min"
        ),
        DiffOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n6", "n7"]),
            field="Revenue in million euros",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[]),
            group="Broadcasting"
        ),
        FindExtremumOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n9"]),
            field="Revenue in million euros",
            which="max"
        ),
        FindExtremumOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n9"]),
            field="Revenue in million euros",
            which="min"
        ),
        DiffOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n10", "n11"]),
            field="Revenue in million euros",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        CompareOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=["n4", "n8"]),
            field="Revenue in million euros",
            which="max",
            targetA="ref:n4",
            targetB="ref:n8"
        ),
        CompareOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n12", "n13"]),
            field="Revenue in million euros",
            which="max",
            targetA="ref:n12",
            targetB="ref:n13"
        )
    ]
}


spec_bhaqrpqx0hwtcol5 = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Life expectancy in years",
            by="Region",
            groupA="Canada",
            groupB="Northwest Territories"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Life expectancy in years",
            which="max"
        )
    ]
}


spec_b1jrtiwi2x01zdtw = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["2005"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            group="Engaged"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            group="Actively disengaged"
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"]),
            field="Share of respondents",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ]
}


spec_bfi0ia7zx8pjb5g8 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group=["Hardlines and leisure goods", "Diversified"]
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Share of retail revenue from foreign operations"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[]),
            field="Share of retail revenue from foreign operations",
            operator=">",
            value=60
        ),
        CountOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"]),
            field="Year"
        )
    ]
}


spec_ahxo354yj7g4m6h1 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Year",
            include=["2000"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[]),
            field="Year",
            include=["2010"]
        ),
        ScaleOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"]),
            target="ref:n1",
            factor=2000000000
        ),
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"]),
            target="ref:n2",
            factor=2000000000
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3", "n4"]),
            field="Percentage of GDP",
            targetA="ref:n3",
            targetB="ref:n4"
        ),
        ScaleOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"]),
            target="ref:n5",
            factor=1/162000000000
        ),
        ScaleOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n6"]),
            target="ref:n6",
            factor=100
        )
    ]
}


spec_apsxmes1emdu9vtk = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            group="0–19 years"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Revenue in million euros",
            which="max"
        ),
        FindExtremumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"]),
            field="Revenue in million euros",
            which="min"
        ),
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"]),
            field="Revenue in million euros",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[]),
            group="20–39 years"
        ),
        FindExtremumOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"]),
            field="Revenue in million euros",
            which="max"
        ),
        FindExtremumOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n5"]),
            field="Revenue in million euros",
            which="min"
        ),
        DiffOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n6", "n7"]),
            field="Revenue in million euros",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[]),
            group="40–59 years"
        ),
        FindExtremumOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n9"]),
            field="Revenue in million euros",
            which="max"
        ),
        FindExtremumOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n9"]),
            field="Revenue in million euros",
            which="min"
        ),
        DiffOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n10", "n11"]),
            field="Revenue in million euros",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        FilterOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=[]),
            group="60–79 years"
        ),
        FindExtremumOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n13"]),
            field="Revenue in million euros",
            which="max"
        ),
        FindExtremumOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=["n14"]),
            field="Revenue in million euros",
            which="min"
        ),
        DiffOp(
            id="n16",
            meta=OpsMeta(nodeId="n12", inputs=["n14", "n15"]),
            field="Revenue in million euros",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        FilterOp(
            id="n17",
            meta=OpsMeta(nodeId="n17", inputs=[]),
            group="80 years and older"
        ),
        FindExtremumOp(
            id="n18",
            meta=OpsMeta(nodeId="n18", inputs=["n17"]),
            field="Revenue in million euros",
            which="max"
        ),
        FindExtremumOp(
            id="n19",
            meta=OpsMeta(nodeId="n19", inputs=["n17"]),
            field="Revenue in million euros",
            which="min"
        ),
        DiffOp(
            id="n20",
            meta=OpsMeta(nodeId="n20", inputs=["n14", "n15"]),
            field="Revenue in million euros",
            targetA="ref:n2",
            targetB="ref:n3"
        ),
        CompareOp(
            id="n21",
            meta=OpsMeta(nodeId="n21", inputs=["n4", "n8"]),
            field="Revenue in million euros",
            which="min",
            targetA="ref:n4",
            targetB="ref:n8"
        ),
        CompareOp(
            id="n22",
            meta=OpsMeta(nodeId="n22", inputs=["n8", "21"]),
            field="Revenue in million euros",
            which="min",
            targetA="ref:n8",
            targetB="ref:n21"
        ),
        CompareOp(
            id="n23",
            meta=OpsMeta(nodeId="n23", inputs=["n12", "n22"]),
            field="Revenue in million euros",
            which="min",
            targetA="ref:n12",
            targetB="ref:n22"
        ),
        CompareOp(
            id="n24",
            meta=OpsMeta(nodeId="n24", inputs=["n16", "n23"]),
            field="Revenue in million euros",
            which="min",
            targetA="ref:n16",
            targetB="ref:n23"
        ),
        CompareOp(
            id="n25",
            meta=OpsMeta(nodeId="n25", inputs=["n20", "n24"]),
            field="Revenue in million euros",
            which="min",
            targetA="ref:n20",
            targetB="ref:n24"
        ),
        
    ]
}



spec_1hp11sl0mo4ohtpo = {
    "ops": [
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Average ticket price in US dollars"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Average ticket price in US dollars",
            which="max"
        )
    ]
}


spec_1it2ia9kmdihxan8 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[]),
            field="Number of incidents",
            operator=">",
            value=50
        ),
        CountOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"]),
            field="Year"
        )
    ]
}


spec_0a2itmazs9jgmmgh = {
    "ops": [
        
    ]

}

spec_0asi8pbitsbxnodv = {
    "ops": [

    ]
}


spec_0cnwglgcwmsbhp4g = {
    "ops": [

    ]
}


spec_0cy2ufyjsinsswpm = {
    "ops": [

    ]
}


spec_0dpnq3twj5hqhd53 = {
    "ops": [

    ]
}


spec_0gehf5045207236n = {
    "ops": [

    ]
}


spec_0gt3h2146jc47ovx = {
    "ops": [

    ]
}


spec_0haw38g4veha18pm = {
    "ops": [

    ]
}


spec_0ijwrg723j4v8s3e = {
    "ops": [

    ]
}


spec_0ivzc37gi49isy9n = {
    "ops": [

    ]
}


spec_1g17ep9vho38jvcz = {
    "ops": [

    ]
}


spec_1g95in84ywix6pcf = {
    "ops": [

    ]
}


spec_1gdzafocxmz7rswi = {
    "ops": [

    ]
}


spec_1hlsoeyqlr1r1n41 = {
    "ops": [

    ]
}


spec_1j86ensex8nyvdyk = {
    "ops": [

    ]
}



spec_1jgaguuh4rqlk7sq = {
    "ops": [

    ]
}


spec_1lf1h5jf9ymeid5q = {
    "ops": [

    ]
}


spec_1lg9qn6shf8ifsdq = {
    "ops": [

    ]
}


spec_1lxkhjyirlc8ghzj = {
    "ops": [

    ]
}




spec_1nhvdb1l9awjyxs1 = {
    "ops": [

    ]
}

spec_1xj7x49epprmpod7 = {
    "ops": [

    ]
}


spec_20lb7iojghs85r21 = {
    "ops": [

    ]
}


spec_21klhgimadx4zsi9 = {
    "ops": [

    ]
}


spec_2203wq7kgv5ha9fi = {
    "ops": [

    ]
}


spec_263367gingx3k5hu = {
    "ops": [

    ]
}


spec_273wm22z47ptlhzz = {
    "ops": [

    ]
}


spec_2a7luy1tzrplr2as = {
    "ops": [

    ]
}


spec_2ecy6apyrdfpoqbo = {
    "ops": [

    ]
}


spec_2jwbvymb2n0i24la = {
    "ops": [

    ]
}



spec_2qd9vs1accbshk2g = {
    "ops": [

    ]
}


spec_2qwuzopitv6gea9l = {
    "ops": [

    ]
}


spec_2r83eabrn5muyizm = {
    "ops": [

    ]
}


spec_2un131viqyjzg34y = {
    "ops": [

    ]
}


spec_2v5t32vooc6fjci1 = {
    "ops": [

    ]
}


spec_2wg6j8htdy5xge6g = {
    "ops": [

    ]
}



spec_31d6673lje5rb1nw = {
    "ops": [

    ]
}


spec_3have0aoq4pehoet = {
    "ops": [

    ]
}


spec_3na7qc2587mdrbox = {
    "ops": [

    ]
}


spec_3nayzu649p458g9n = {
    "ops": [

    ]
}


spec_4623mdsdv9ewvlb7 = {
    "ops": [

    ]
}


spec_4j7o14z979o5bq5d = {
    "ops": [

    ]
}


spec_50pei8jwlb2g5h1q = {
    "ops": [

    ]
}


spec_56010lp5kjl1p4by = {
    "ops": [

    ]
}


spec_58wxo6da4x2w1ass = {
    "ops": [

    ]
}


spec_5ldzsatw0rpbpxz3 = {
    "ops": [

    ]
}



spec_5rjyoxyictwaceaz = {
    "ops": [

    ]
}


spec_6i84fq1ot2j0njaf = {
    "ops": [

    ]
}


spec_6macy6l6h00wvng7 = {
    "ops": [

    ]
}


spec_71v97x2ifsxw6u8p = {
    "ops": [

    ]
}


spec_77xb5ug5lhfmkb74 = {
    "ops": [

    ]
}



spec_7iy5s09teyeaybzy = {
    "ops": [

    ]
}


spec_7mw5410egrxfi2oy = {
    "ops": [

    ]
}


spec_7rsc3a0rw1rlh7pk = {
    "ops": [

    ]
}


spec_83hx57gqlkd9sldn = {
    "ops": [

    ]
}


spec_87b7sitfbe4ttuns = {
    "ops": [

    ]
}


spec_88sup9tkwx0lwkgw = {
    "ops": [

    ]
}


spec_8glm4qrzc2cbbq1e = {
    "ops": [

    ]
}


spec_8mntkwdil1gq6xzh = {
    "ops": [

    ]
}


spec_8n0916e3z0epuuyi = {
    "ops": [

    ]
}


spec_8rl54wqvzm1olimr = {
    "ops": [

    ]
}


spec_90tonvacpe7zniv9 = {
    "ops": [

    ]
}


spec_9g5a38vcep03acdu = {
    "ops": [

    ]
}


spec_9g9t9lbwhc8yp623 = {
    "ops": [

    ]
}


spec_9hgt5h53p4ic33md = {
    "ops": [

    ]
}


spec_9r3kyy2jo2o66msh = {
    "ops": [

    ]
}


spec_9r7co7yl1osn3zg4 = {
    "ops": [

    ]
}


spec_9sdl1j9l1fbhwq09 = {
    "ops": [

    ]
}


spec_a0m3af45az33ngmr = {
    "ops": [

    ]
}


spec_a6gnu78mgn3xmqhu = {
    "ops": [

    ]
}


spec_a7byilpdrc3cbjr4 = {
    "ops": [

    ]
}


spec_ae2xp7bacbbs0kmx = {
    "ops": [

    ]
}


spec_avwb8xstxx1lmfpk = {
    "ops": [

    ]
}


spec_awg12vb36ndo75tq = {
    "ops": [

    ]
}


spec_b4o9bh8f969q6kqa = {
    "ops": [

    ]
}


spec_b8um9hhxelrqowd9 = {
    "ops": [

    ]
}


spec_b9vfcqsqid200mah = {
    "ops": [

    ]
}


spec_bd95lx2pntlr7ati = {
    "ops": [

    ]
}


spec_bhqzjnykymk43yqi = {
    "ops": [

    ]
}


spec_bkemtvekxtnuk8bf = {
    "ops": [

    ]
}


spec_bnil22qu3wwatrc7 = {
    "ops": [

    ]
}


spec_bpmaqi8nt785y4ay = {
    "ops": [

    ]
}


spec_c1dkepdvg39l54su = {
    "ops": [

    ]
}


spec_c3mncg8r4g6bjoon = {
    "ops": [

    ]
}


spec_c41fny6w7gwpawbn = {
    "ops": [

    ]
}


spec_c7pc0uciecc5secj = {
    "ops": [

    ]
}


spec_cby91tt3tvahsmuj = {
    "ops": [

    ]
}


spec_chrkcwjl9vro8a6o = {
    "ops": [

    ]
}


spec_ciqofa9lr4z5kz7d = {
    "ops": [

    ]
}


spec_ckptmodbya2m1mih = {
    "ops": [

    ]
}


spec_ddnda3bjdstiwf90 = {
    "ops": [

    ]
}


spec_dn0vscuua02yn80x = {
    "ops": [

    ]
}


spec_f12st3qo0kz1egmp = {
    "ops": [

    ]
}


spec_fsraebh4cpmzc7ut = {
    "ops": [

    ]
}


spec_g1s9b91z7xw8flg2 = {
    "ops": [

    ]
}


spec_gnin1xu8b8rbtv34 = {
    "ops": [

    ]
}


spec_guhd9zsodg7n408g = {
    "ops": [

    ]
}


spec_h33j4k50c44wni7l = {
    "ops": [

    ]
}


spec_i0fd8sbi945erf7p = {
    "ops": [

    ]
}


spec_rx7zzpt8c0ue86y3 = {
    "ops": [

    ]
}
