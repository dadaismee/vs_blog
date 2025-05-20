---
id: index
aliases: []
tags: []
date: "26.04.2025"
generate_toc: true
summary: pook
title: Живые клетки, наука о данных и «второй мозг» (1/3)
---

## Клетки-аналитики данных

- Живые клетки ведут себя как аналитики данных.


Adjust the slider: [slider min=0 max=100 var=sliderValue value=50]

Current value is {{ sliderValue }}.

<div v-scope="{ count: 0 }">
  <span v-text="count"></span>
  <button v-on:click="count++">increase</button>
</div>

Drag to adjust values:

- The font size is currently {{size}}px [slider min=8 max=72 var=size]
- The spacing between lines is {{spacing}}em ([slider min=0.8 max=3 var=spacing value=1.5 step=0.1])
- The color opacity is {{opacity}}% ([slider min=0 max=100 var=opacity value=100])

<div style="font-size:{{size}}px; line-height:{{spacing}}em; opacity:{{opacity/100}}">
  This text changes dynamically as you adjust the sliders!
</div>


























       +-------------------+
       |    Semi-Closed    |
       |      System       |
       +-------------------+
              A    |
              |    v
          Input    Output

<br> 

## Network of semi-closed systems
       +------------------+           +------------------+
       |     Village 1    |<--------->|     Village 2    |
       +--------A---------+           +---------A--------+
                |                               |
       +--------v---------+           +---------V--------+
       |     Village 3    |           |     Village 4    |
       +------------------+           +------------------+

<br>

## Inputs and outputs
       +------------------+           +------------------+
       |     Деревня 1    |<--------->|     Деревня 2    |
       +--------A---------+           +---------A--------+
                |             ТОВАРЫ            |
                |             ДАННЫЕ            |
       +--------v---------+           +---------V--------+
       |     Деревня 3    |           |     Деревня 4    |
       +------------------+           +------------------+

<br>

## Uniqueness indebted to adaptation
- adaptation to flora and fauna
- locally relevant skills
- cures to endemic diseases

<br>

## Each village is unique

           .--.                     .--.            
       .-(       ).             .-(    ).         
      (__ Village 1_)       (__Village 2_)      
          `-..-'                 `-..-'          

           ,--.       
        ,-'    `-.          
       /            \       +------v-------+           
      |   Village 3  |      |   Village 4  |          
       \            /       +--------------+          
        `-.____.-'        

<br>

## But they share data

           .--.                     .--.            
       .-(       ).             .-(    ).         
      (__ Village 1_)       (__Village 2_)      
          `-..-'                 `-..-'          

           ,--.       DATA             
        ,-'    `-.          
       /            \       +------v-------+           
      |   Village 3  |      |   Village 4  |          
       \            /       +--------------+          
        `-.____.-'        

<br>

## Which data is networked 

           .--.                     .--.            
       .-(       ).             .-(    ).         
      (__ Village 1_)       (__Village 2_)      
          `-..-'                 `-..-'          
                     ANTI-BODIES
           ,--.    LOCAL NUTRIENTS
        ,-'    `-.  LOCAL SKILLS          
       /            \       +------v-------+           
      |   Village 3  |      |   Village 4  |          
       \            /       +--------------+          
        `-.____.-'        

<br>

## Skills are distributed

       +------------------+           +------------------+
       |████████ Village 1|-----------|█    Village 2    |
       +--------+---------+           +---------+--------+
                |                               |
                |          WOODWORKING          |
                |                               |
       +--------v---------+           +------------------+
       |████ Village 3    |           |██████████████████|
       +------------------+           +------------------+

<br>

## Health is distributed
       +------------------+           +------------------+
       |█████ Village 1   |-----------|██   Village 2    |
       +--------+---------+           +---------+--------+
                |                               |
                |            IMMUNITY           |
                |                               |
       +--------v---------+           +------------------+
       |████████ Village 3|           |███   Village 4   |
       +------------------+           +------------------+

<br>

## Storage units are local and distributed

           ____________________________
          /                          / |
         /__________________________/  |
        |██████████████████████████|   |
        |██████████████████████████|   |
        |      VILLAGE SERVER      |   |
        |██████████████████████████|   /
        |██████████████████████████|  /
        |__________________________| /
        |__________________________|

