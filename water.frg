#lang forge/temporal

// Our discrete states for water quality and plant growth
enum WaterQualityState { Low, Medium, High }
enum PlantGrowthState { Sparse, Moderate, Dense }

// Signature for Zebra Mussels with a property to indicate whether they are juveniles or adults
sig ZebraMussel {
    //if a mussel is juvenile, it filters less water
    isJuvenile: one Boolean
}

// Signature for Water Quality using discrete states
sig WaterQuality {
    clarity: one WaterQualityState
}

// Signature for Plant Growth using discrete states
sig PlantGrowth {
    growthState: one PlantGrowthState
}

// Main model signature for a Lake that contains Zebra Mussels, Water Quality, and Plant Growth
temporal sig Lake {
    mussels: set ZebraMussel,
    waterQuality: one WaterQuality,
    plants: one PlantGrowth
}

// Initial conditions: Assuming the lake starts with medium water clarity and moderate plant growth
fact initConditions {
    init (this.waterQuality.clarity = Medium)
    init (this.plants.state = Moderate)
}

// Temporal dynamics describing how Zebra Mussel populations influence water quality and plant growth
fact dynamics {
    // If mussel population increases, clarity transitions from Low to Medium or Medium to High
    always (this.mussels.count() > 20 and this.mussels.count() <= 50 implies next_state (this.waterQuality.clarity = Medium))
    always (this.mussels.count() > 50 implies next_state (this.waterQuality.clarity = High))

    // If mussel population decreases, clarity might degrade
    always (this.mussels.count() < 20 implies next_state (this.waterQuality.clarity = Low))

    // Plant growth response to changes in water quality
    always (this.waterQuality.clarity = High implies next_state (this.plants.state = Dense))
    always (this.waterQuality.clarity = Low implies next_state (this.plants.state = Sparse))
    always (this.waterQuality.clarity = Medium implies next_state (this.plants.state = Moderate))
}

// Run scenarios to check model behavior under different mussel population levels
run checkDynamics for 10 but 100 ZebraMussel, 3 Lake
