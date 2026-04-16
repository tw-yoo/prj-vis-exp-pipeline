from opsspec.specs import *

spec_1bv05pu9d8jnidty = {
    "ops":[
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2020", "2021", "2022", "2023", "2024", "2025"]
        ),
        CountOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Year"
        )
    ],
    "ops2":[
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="National debt in billion US dollars"
        )
    ],
    "ops3":[
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            target="ref:n3",
            factor=1/6
        )
    ]
}


spec_2mi8b2r0oalayl6g = {
    "ops": [
        # Find all the year-by-year values of the playoff teams

    ],
    "ops2": [
        # Find all the annual values of all teams
    ],
    "ops3": [
        # Sum the values by year
    ],
    "ops4": [
        # Sort the subtracted values in ascending order
    ],
    "ops5": [
        # Find the first value
    ]
}

spec_82aqt0k0jnbj3irf = {
    "ops": [
        # count the number of enterprises in each year
    ],
    "ops2": [
        # Sort in ascending order
        SortOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=2),
            field="Number of enterprises",
            order="asc"
        )
    ],
    "ops3": [
        # Find the year of the fifth value
        NthOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=3),
            field="Number of enterprises",
            n=5
        )
    ]
}

spec_1jatwi94v2d8cr9u = {
    "ops": [
        # Sum all the annual values of the digital market
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Digital market"
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Value in billion US dollars"
        )
    ],
    "ops2": [
        # Sum all the annual values of the package market
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            group="Package market"
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Value in billion US dollars"
        )
    ],
    "ops3": [
        # Find the difference between the two values
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n2", inputs=["n2", "n4"], sentenceIndex=3),
            field="Value in billion US dollars",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}

spec_2bhsybiilde28j87 = {
    "ops": [
        # Find the values of white, hispanic, and other very interested
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Race_Ethnicity",
            include=["White", "Hispanic", "Other"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            group="Very interested"
        )
    ],
    "ops2": [
        # Sum all these values
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Share_of_Respondents"
        )
    ],
    "ops3": [
        # Divide by three
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            target="ref:n3",
            factor=1/3
        )
    ]
}

spec_1bywaj7stsb3060c = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Company",
            include=["MD", "Crai"]
        )
    ],
    "ops2": [
    ],
    "ops3": [
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=3),
            field="Market shares"
        )
    ]
}

spec_6ah60yba8o7rw0i9 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Yoghurt with additives"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Average_Price_Euros",
            which="max"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            group="Yoghurt without additives"
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Average_Price_Euros",
            which="min"
        )
    ],
    "ops3": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Average_Price_Euros",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}

spec_5p6g89v7l99aes05 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Playoff teams"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            group="All teams"
        )
    ],
    "ops3": [
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=3),
            field="Average_Payroll_Million_USD",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ],
    "ops4": [
        SortOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Average_Payroll_Million_USD",
            order="desc"
        )
    ],
    "ops5": [
        NthOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Average_Payroll_Million_USD",
            n=1
        )
    ]
}

spec_1ce802l2rdg98d7d = {
    "ops": [
        SortOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share of respondents",
            order="desc"
        )
    ],
    "ops2": [
        NthOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Share of respondents",
            n=3
        )
    ]
}

spec_1hokbw2gmzar9ye8 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="60 years and over"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Group",
            include=["Women"]
        ),

    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            group=["18 years and over", "18 to 39 years"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=2),
            field="Group",
            include=["Men"]
        ),
    ],
    "ops3": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
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
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Female"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Number_of_Victims",
            which="max"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            group="Male"
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Number_of_Victims",
            which="min"
        )
    ],
    "ops3": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Number_of_Victims",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}

spec_8e9wp443ff1i6snq = {
    "ops": [
    ],
    "ops2": [
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=2),
            field="Immigration rate per thousand inhabitants"   
        )
    ],
    "ops3": [
        SortOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=3),
            field="Immigration rate per thousand inhabitants",
            order="desc"
        )
    ],
    "ops4": [
        NthOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Immigration rate per thousand inhabitants",
            n=1
        )
    ]
}

spec_2n0g3tsz1rsz6fgr = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Industry"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Year",
            include=["2010", "2015", "2020"]
        ),
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Share of total employment"
        )
    ],
    "ops3": [
        SortOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            field="Share of total employment",
            order="desc"
        )
    ],
    "ops4": [
        NthOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=4),
            n=1
        )
    ]
}

spec_8chfa8n079zpfigi = {
    "ops": [
    ],
    "ops2": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="FIFA World Ranking position",
            operator="between",
            value=["20", "30"]
        ),
        CountOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Year"
        )
    ]
}

spec_1j7gx35h6i9mpi6j = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Item",
            include=["Beauty products"]
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Item",
            include=["Books"]
        )
    ],
    "ops3": [
        # Subtract two values
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ]
}

spec_2yech0pea1xihind = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Platform",
            include=["META"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            group="Several times a day"
        ),
        
    ],
    "ops2": [
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
            field="Percentage"
        )
    ]
}

spec_64ue1v00wj8vg48e = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            include=["1996", "1999", "2004", "2005", "2006", "2007", "2008", "2009"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            group="Should be valid"
        ),
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            field="Share of respondent"
        )
        
    ],
    "ops2": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            include=["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            group="Should be valid"
        ),
        AverageOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=2),
            field="Share of respondent"
        )
    ],
    "ops3": [
        DiffOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n3", "n6"], sentenceIndex=3),
            field="Share of respondent",
            targetA="ref:n3",
            targetB="ref:n6"
        )
    ]
}

spec_1dm30xw1gpjo8ke5 = {
    "ops": [
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share of GDP",
            which="max"
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Share of GDP",
            which="min"
        )
    ],
    "ops3": [
        AverageOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=3),
            field="Share of GDP",
        )
    ]
}

spec_8hiwwys6qkrbtapb = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2002/03", "2003/04", "2004/05", "2005/06", "2006/07", "2007/08", "2008/09", "2009/10"]
        )
    ],
    "ops2": [
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Crime rate per 1,000 population"
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
            field="Year",
            include=["2010/11", "2011/12", "2012/13", "2013/14", "2014/15", "2015/16", "2016/17", "2017/18", "2018/19", "2019/20"]
        )
    ],
    "ops4": [
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=4),
            field="Crime rate per 1,000 population"
        )
    ],
    "ops5": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=5),
            field="Crime rate per 1,000 population",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}

spec_1mzcynif2s4mm6ps = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Enterprises"
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Share of respondents"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            group="Provider"
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Share of respondents"
        )
    ],
    "ops3": [
        # Find the difference between the two values
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=3),
            field="Share of respondents",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}

spec_54gh54f24irr63pb = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2018"]
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            group="Party_Advantage",
            which="min"
        )
    ],
    "ops3": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            group="Party_Advantage",
            which="min"
        )
    ]
}

spec_1p6uue3hxdxit3ey = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="30 to 44 years"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Response",
            include=["Yes"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=2),
            field="Response",
            include=["No"]
        ),
        CompareOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=2),
            field="Response",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ]
}

spec_1fngt6cb1d60a2ow = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Number of employees",
            exclude=["Metro Total"]
        ),
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Number of employees"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Number of employees",
            operator="<",
            value=50000,

        )
    ]
}

spec_6rvtt4egfl5nmyue = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="female"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Year",
            include=["2012", "2013", "2014", "2015", "2016", "2017"]
        )
    ],
    "ops3": [
        SortOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="",
            order="desc"
        )
    ],
    "ops4": [
        NthOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=4),
            n=2
        )
    ]
}

spec_1suppecte0dm69gm = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Not at all"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Respondent Group",
            include=["Women"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Respondent Group",
            include=["Men"]
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=1),
            field="Percentage of respondents"
        )
    ],
    "ops2": [
        ScaleOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=2),
            target="ref:n4",
            factor=1/2
        )
    ],
    "ops3": [
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1"], sentenceIndex=3),
            field="Respondent Group",
            include=["All adults"]
        )
    ]
}

spec_1e56qqj7moat9gqa = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Fiscal Year & Status",
            include=["FY 2017 Actual"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Fiscal Year & Status",
            include=["FY 2018 Actual"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            field="Fiscal Year & Status",
            include=["FY 2019 Actual"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=1),
            field="Fiscal Year & Status",
            include=["FY 2020 Actual"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=1),
            field="Fiscal Year & Status",
            include=["FY 2021 Actual"]
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1"], sentenceIndex=1),
            field="Spending in billion US dollars",
            operator="==",
            value="ref:n1"
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n2"], sentenceIndex=1),
            field="Spending in billion US dollars",
            operator="==",
            value="ref:n2"
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n3"], sentenceIndex=1),
            field="Spending in billion US dollars",
            operator="==",
            value="ref:n3"
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n4"], sentenceIndex=1),
            field="Spending in billion US dollars",
            operator="==",
            value="ref:n4"
        ),
        CountOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n6"], sentenceIndex=1),
            field="Fiscal Year & Status"
        ),
        CountOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n7"], sentenceIndex=1),
            field="Fiscal Year & Status"
        ),
        CountOp(
            id="n12",
            meta=OpsMeta(nodeId="n12", inputs=["n8"], sentenceIndex=1),
            field="Fiscal Year & Status"
        ),
        CountOp(
            id="n13",
            meta=OpsMeta(nodeId="n13", inputs=["n9"], sentenceIndex=1),
            field="Fiscal Year & Status"
        ),
        FilterOp(
            id="n14",
            meta=OpsMeta(nodeId="n14", inputs=["n10", "n11", "n12", "n13"], sentenceIndex=1),
            operator=">",
            value=1
        )
    ],
    "ops2": [
        SumOp(
            id="n15",
            meta=OpsMeta(nodeId="n15", inputs=["n14"], sentenceIndex=1),
            field="Spending in billion US dollars"
        )
    ]
}

spec_6p4fnscalopvysnn = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share of the population",
            operator=">",
            value=40
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Share of the population",
            which="max"
        )
    ]
}

spec_50y71e5i2n28gkbx = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2017", "2018"]
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            group=["Sportswear", "Running"]
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Revenue_Million_USD"
        )
    ],
    "ops3": [
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            target="ref:n3",
            factor=1/2
        )
    ]
}

spec_75yz7pci1w1dif3g = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="None of these"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            group="Cheese and onion"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Age_Group",
            include=["18–24"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n1"], sentenceIndex=1),
            field="Age_Group",
            include=["25–39"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n1"], sentenceIndex=1),
            field="Age_Group",
            include=["40–59"]
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n1"], sentenceIndex=1),
            field="Age_Group",
            include=["60 +"]
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n2"], sentenceIndex=1),
            field="Age_Group",
            include=["18–24"]
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n2"], sentenceIndex=1),
            field="Age_Group",
            include=["25–39"]
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n2"], sentenceIndex=1),
            field="Age_Group",
            include=["40–59"]
        ),
        FilterOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n2"], sentenceIndex=1),
            field="Age_Group",
            include=["60 +"]
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=[], sentenceIndex=2),
            field="Share_of_Respondents",
            which="max",
            rank=3
        )
    ]
}

spec_7extlfw651gqc5fk = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Large"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Percentage",
            which="max"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=1),
            group="Large"
        ),
        FindExtremumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=1),
            field="Percentage",
            which="min"
        )
    ],
    "ops2": [
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            field="Percentage",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ],
    "ops3": [
        AverageOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=3),
            field="Percentage"
        )
    ],
    "ops4": [
        CompareOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=4),
            field="Percentage",
            targetA="ref:n5",
            targetB="ref:n6"
        )
    ]
}

spec_6rqevjp16hadlyly = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2007/08"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2011/12"]
        )
    ],
    "ops2": [
        CompareOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Percentage of tests passed",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ]
}

spec_1esx2fbduhqn7knk = {
    "ops": [
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Deaths",
            which="max"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Deaths",
            which="min"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Deaths",
            exclude=["ref:n1", "ref:n2"]
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Deaths",
        )
    ],
    "ops3": [
        ScaleOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            target="ref:n4",
            factor=1/4
        )

    ]
}

spec_1epzpacytv3wx2i6 = {
    "ops": [
        # Find the 2010 and 2013 values
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
            include=["2010"]
        )
    ],
    "ops2": [
        # Verify that the size values are rising
        LagDiffOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1", "n2"]),
            field="Market size in million GBP",
            
        )
    ]
}

spec_1qm2z3ooawf339jz = {
    "ops": [
        # Add East and Scotland values for each response
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="England (NET)"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            group="Scotland"
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            field="Share of respondents"
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=1),
            field="Share of respondents"
        )
    ],
    "ops2": [
        # Compare the additional values
        CompareOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3", "n4"], sentenceIndex=2),
            field="Share of respondents",
            targetA="ref:n3",
            targetB="ref:n4",
            which="max"
        )
    ]
}

spec_95yhyqjyeu4fohbj = {
    "ops": [
        # Add the minimum and maximum values
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Number of people in millions",
            which="min"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Number of people in millions",
            which="max"
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=1),
            field="Number of people in millions"
        )
    ],
    "ops2": [
        # Divide the added value by two
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            target="ref:n3",
            factor=1/2
        )
    ],
    "ops3": [
        # Find the value for 2010
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=3),
            include=["2010"]
        )
    ],
    "ops4": [
        # Compare the value in 2010 with the average value added
        CompareOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n4", "n5"], sentenceIndex=4),
            field="Number of people in millions",
            targetA="ref:n4",
            targetB="ref:n5",
            which="max"
        )
    ]
}

spec_62w3xg16iivw11et = {
    "ops": [
        # Add to the Industry values of the 2010s
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Industry"
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Year",
            include=["2010"]
        ),
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=1),
            field="Share_of_GDP"
        )
    ],
    "ops2": [
        # Divide the added Industry values by the number of years
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            field="Share_of_GDP",
            target="ref:n3",
            factor=1/2
        )
    ],
    "ops3": [
        # Add the services values from the 2010s
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Share_of_GDP"
        )
    ],
    "ops4": [
        # Divide the additional Services values by the number of years
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=4),
            group="Industry"
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n5"], sentenceIndex=4),
            field="Year",
            include=["2010"]
        ),
        SumOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n6"], sentenceIndex=4),
            field="Share_of_GDP"
        )
    ],
    "ops5": [
        # Compare the two values
        CompareBoolOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n4", "n7"], sentenceIndex=5),
            field="Share_of_GDP",
            operator="==",
            targetA="ref:n4",
            targetB="ref:n7"
        )
    ]
}

spec_95wcyze391ifhegp = {
    "ops": [
        # Find the highest and lowest values
        FindExtremumOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Exchange rate in Singapore dollars",
            which="max"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=1),
            field="Exchange rate in Singapore dollars",
            which="min"
        )
    ],
    "ops2": [
        # Add the value obtained
        SumOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Exchange rate in Singapore dollars",
        )
    ],
    "ops3": [
        # Divide the value by 2
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            target="ref:n3",
            factor=1/2
        )
    ]
}

spec_9douccar3m9ruah4 = {
    "ops": [
        # Add Men's Not at all value and Women's Not at all value
    ],
    "ops2": [
        # Divide the added value by two
    ],
    "ops3": [
        # Compare to the All results value
    ]
}

spec_9mlpjn6pddrbthj8 = {
    "ops": [
        SortOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Number of fatalities",
            order="asc"
        )
    ],
    "ops2": [
        NthOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            n=3
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
            field="Year",
            include=["2011", "2012"]
        ),
        AverageOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            field="Number of fatalities"
        )
    ],
    "ops4": [
        CompareBoolOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n2", "n4"], sentenceIndex=4),
            operator=">",
            targetA="ref:n2",
            targetB="ref:n4"
        )
    ]
}

spec_1x37jzohqd666qc0 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Don't know/no opinion"
        ),
        AverageOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Percentage of respondents"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            group="Very unlikely"
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Category",
            include=["Family"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            field="Category",
            include=["Local community"]
        ),
        DiffOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n4", "n5"], sentenceIndex=2),
            field="Percentage of respondents",
            targetA="ref:n4",
            targetB="ref:n5"
        )
    ],
    "ops3": [
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=3),
            group="Somewhat unlikely"
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=[], sentenceIndex=3),
            field="Category",
            include=["Family"]
        ),
        FilterOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=[], sentenceIndex=3),
            field="Category",
            include=["Local community"]
        ),
        DiffOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n8", "n9"], sentenceIndex=3),
            field="Percentage of respondents",
            targetA="ref:n8",
            targetB="ref:n9"
        )

    ],
    "ops4": [
        SumOp(
            id="n11",
            meta=OpsMeta(nodeId="n11", inputs=["n6", "n10"], sentenceIndex=5),
            field="Percentage of respondents",
        )
    ],
    "ops5": [
        CompareOp(
            id="n12",
            meta=OpsMeta(nodeId="n9", inputs=["n2", "n11"], sentenceIndex=5),
            field="Percentage of respondents",
            targetA="ref:n2",
            targetB="ref:n11"
        )
    ]
}

spec_9u3xwiltv2hlcqq1 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            include=["2007", "2011", "2012"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n1", inputs=["n1"], sentenceIndex=1),
            group="Democratic government"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            group="Strong leader"
        ),
        LagDiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2"], sentenceIndex=1),
            field="Percentage",
            signed=True
        ),
        LagDiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n3"], sentenceIndex=1),
            field="Percentage",
            signed=True
        ),

    ],
    "ops2": [
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=2),
            field="Year",
            include=["2007", "2011", "2012"]
        ),
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=["n6"], sentenceIndex=1),
            group="Democratic government"
        ),
        FilterOp(
            id="n8",
            meta=OpsMeta(nodeId="n8", inputs=["n6"], sentenceIndex=1),
            group="Strong leader"
        ),
        LagDiffOp(
            id="n9",
            meta=OpsMeta(nodeId="n9", inputs=["n7"], sentenceIndex=1),
            field="Percentage",
            signed=True
        ),
        LagDiffOp(
            id="n10",
            meta=OpsMeta(nodeId="n10", inputs=["n8"], sentenceIndex=1),
            field="Percentage",
            signed=True
        ),
        
    ]
}

spec_1hv85ef35tbvldiq = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Revenue in billion US dollars",
            operator="==",
            value=2.0
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            include=["2010", "2019", "2020"]
        )
    ],
    "ops3": [
        # 3 years
        CountOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=3),
            field="Year"
        )
    ]
}

spec_au22oa0vjosoagxu = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="male"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Year",
            include=["2014"]
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=3),
            field="Year",
            value=["2008", "2014"]
        )
    ]
}

spec_albgfrf44bz6134k = {
    "ops": [
        AverageOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Inhabitants in millions"
        )
    ],
    "ops2": [
        LagDiffOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Inhabitants in millions",
            order="desc",
            signed=True
        ),
        CompareBoolOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=2),
            field="Inhabitants in millions",
            operator="==",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ]
}

spec_23bplnbw291p6nil = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Age_Group",
            include=["50 to 59"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            group="Female"
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=1),
            group="Male"
        )
    ],
    "ops2": [
        DiffOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=2),
            field="Median_Annual_Pay_GBP",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ]
}

spec_aoycx517slbw0ifa = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Year",
            exclude=["2019", "2020"]
        )
    ],
    "ops2": [
        SumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Revenue in million euros"
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=3),
            group="Entertainment division"
        ),
        SumOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=3),
            field="Revenue in million euros"
        )
    ]
}

spec_aqowly2mmavof3f1 = {
    "ops": [
        # find the longest domain range without increase
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Unemployment rate",
            order="asc",
            signed=True
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Unemployment rate",
            operator="<",
            value=0
        )
    ],
    "ops2": [
        # 2011-2019
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=3),
            operator="between",
            value=["2011", "2019"]
        )
    ]
}

spec_23zc8kuhnpespj98 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Boy"
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Share_of_Respondents"
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=3),
            field="Genre",
            include=["Comedy"]
        )
    ]
}

spec_1hm06wtar7gh92c8 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Share of population older than 65 years old",
            operator="==",
            value=0.065
        )
    ],
    "ops2": [
        ScaleOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            target="ref:n1",
            factor=100000
        )
    ]
}

spec_amn6abwhwmc7ksaz = {
    "ops": [
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Price in US dollars per peak watt",
            signed=True
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Quarter/Year",
            include=["Q1 '16", "Q2 '16", "Q3 '16",  "Q4 '16"]
        ),
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            field="Quarter/Year",
            include=["Q1 '17", "Q2 '17", "Q3 '17", "Q4 '17"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            field="Quarter/Year",
            include=["Q1 '18", "Q2 '18", "Q3 '18", "Q4 '18"]
        ),
        FilterOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            field="Quarter/Year",
            include=["Q1 '19", "Q2 '19", "Q3 '19", "Q4 '19"]
        ),
        FilterOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=[], sentenceIndex=2),
            field="Quarter/Year",
            include=["Q1 '20", "Q2 '20", "Q3 '20"]
        )
    ],
    "ops3": [
        FilterOp(
            id="n7",
            meta=OpsMeta(nodeId="n7", inputs=[], sentenceIndex=3),
            field="Quarter/Year",
            include=["Q1 '17", "Q2 '17", "Q3 '17", "Q4 '17"]
        )
    ]
}

spec_221xoyhy3yziwabm = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="2014"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Satisfaction_Level",
            include=["Very satisfied", "Somewhat satisfied"]
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1"], sentenceIndex=3),
            field="Satisfaction_Level",
            include=["Somewhat dissatisfied", "Very dissatisfied"]
        )
    ],
    "ops4": [
        CompareOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n2", "n3"], sentenceIndex=4),
            field="Satisfaction_Level",
            which="max",
            targetA="ref:n2",
            targetB="ref:n3"
        )
    ]
}

spec_25n4mzhv6y1p36dl = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Spend more"
        )
    ],
    "ops2": [
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=2),
            field="Share_of_Respondents",
            which="min"
        )
    ]
}

spec_ay58pwlf97q0osw6 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Source",
            exclude=["Broadcasting"]
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            group="Commercial"
        ),
        DetermineRangeOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Revenue in million euros"
        )
    ],
    "ops3": [
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=3),
            group="Matchday"
        ),
        DetermineRangeOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=3),
            field="Revenue in million euros"
        )
    ],
    "ops4": [
        CompareBoolOp(
            id="n6",
            meta=OpsMeta(nodeId="n6", inputs=["n3", "n5"], sentenceIndex=4),
            field="Revenue in million euros",
            targetA="ref:n3",
            targetB="ref:n5"
        )
    ],
    "ops5": [
        
    ]
}

spec_bhaqrpqx0hwtcol5 = {
    "ops": [
        PairDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Life expectancy in years",
            by="Region",
            groupA="Canada",
            groupB="Northwest Territories"
        )
        
    ]
}

spec_b1jrtiwi2x01zdtw = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="Engaged"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            group="Not engaged"
        )
    ],
    "ops3": [
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=3),
            field="Share of respondents",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ]
}

spec_bfi0ia7zx8pjb5g8 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group=["Hardlines and leisure goods", "FMCG", "Diversified"]
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Share of retail revenue from foreign operations",
            operator="==",
            value=60
        )
    ],
    "ops3": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=3),
            field="Share of retail revenue from foreign operations",
            operator="<",
            value=60
        )
    ]
}

spec_ahxo354yj7g4m6h1 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            include=["2000"]
        ),
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            include=["2010"]
        ),
        DiffOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n1", "n2"], sentenceIndex=3),
            field="Percentage of GDP",
            targetA="ref:n1",
            targetB="ref:n2"
        )
    ],
    "ops2": [
        ScaleOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=["n3"], sentenceIndex=2),
            target="ref:n3",
            factor=20000000000
        )
    ],
    "ops3": [
        ScaleOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=["n4"], sentenceIndex=3),
            target="ref:n4",
            factor=10
        )
    ]
}

spec_apsxmes1emdu9vtk = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            group="80 years and older"
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            include=["2018"]
        )
    ]
}

spec_1hp11sl0mo4ohtpo = {
    "ops": [
        LagDiffOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Average ticket price in US dollars"
        ),
        FindExtremumOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=["n1"], sentenceIndex=1),
            field="Average ticket price in US dollars",
            which="max"
        )
    ],
    "ops2": [
        FilterOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=[], sentenceIndex=2),
            include=["2012/13"]
        ),
        FilterOp(
            id="n4",
            meta=OpsMeta(nodeId="n4", inputs=[], sentenceIndex=2),
            include=["2013/14"]
        ),
        DiffOp(
            id="n5",
            meta=OpsMeta(nodeId="n5", inputs=[], sentenceIndex=2),
            field="Average ticket price in US dollars",
            targetA="ref:n3",
            targetB="ref:n4"
        )
    ]
}

spec_1it2ia9kmdihxan8 = {
    "ops": [
        FilterOp(
            id="n1",
            meta=OpsMeta(nodeId="n1", inputs=[], sentenceIndex=1),
            field="Number of incidents",
            operator="==",
            value=50
        )
    ],
    "ops2": [
        FilterOp(
            id="n2",
            meta=OpsMeta(nodeId="n2", inputs=[], sentenceIndex=2),
            field="Number of incidents",
            operator="<",
            value=50
        ),
        CountOp(
            id="n3",
            meta=OpsMeta(nodeId="n3", inputs=["n2"], sentenceIndex=2),
            field="Year"
        )
    ]
}