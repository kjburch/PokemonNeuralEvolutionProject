import os
import cv2 as cv
import numpy as np
from pokemonEnums import *
from pokemonFunctions import *

scale_percent = 3
template = cv.imread("Images/battleBackground.png")
template = cv.resize(template, (int(template.shape[1] * scale_percent), int(template.shape[0] * scale_percent)),
                     cv.INTER_NEAREST)
# add bottom
b = cv.imread("Images/battleBackgroundBottom.png")
b = cv.resize(b, (int(b.shape[1] * scale_percent), int(b.shape[0] * scale_percent)),
                 cv.INTER_NEAREST)


def overlayImage(img1, img, x, y, mult=1, grey=False):
    p1 = cv.imread(img)
    img2 = cv.resize(p1, (int(p1.shape[1] * scale_percent * mult), int(p1.shape[0] * scale_percent * mult)),
                                 cv.INTER_NEAREST)

    # I want to put logo on top-left corner, So I create a ROI
    rows, cols, channels = img2.shape
    roi = img1[y:y + rows, x:x + cols]
    # Now create a mask of logo and create its inverse mask also
    img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    if mult == 1.5 or mult == 1.1:
        img2gray = cv.filter2D(cv.blur(img2gray,(5,5)),-1,kernel=np.ones((5,5),np.float32)/25)
    ret, mask = cv.threshold(img2gray, 15, 255, cv.THRESH_BINARY)
    mask_inv = cv.bitwise_not(mask)
    # Now black-out the area of logo in ROI
    img1_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
    # Take only region of logo from logo image.
    if grey:
        img2_fg = cv.bitwise_and(img2, img2, mask=mask_inv)
    else:
        img2_fg = cv.bitwise_and(img2, img2, mask=mask)
    # Put logo in ROI and modify the main image
    dst = cv.add(img1_bg, img2_fg)

    img1[y:y + rows, x:x + cols] = dst

    return img1


def showBattle(currentTeam, currentTeamActivePokemon, otherTeam, otherTeamActivePokemon, text, team, turnNum):
    createImage(currentTeam, currentTeamActivePokemon, otherTeam, otherTeamActivePokemon, text, team, turnNum)
    if team == 1:
        team = 2
    else:
        team = 1
    createImage(otherTeam, otherTeamActivePokemon, currentTeam, currentTeamActivePokemon, text, team, turnNum)
    cv.waitKey(0)


def createImage(currentTeam, currentTeamActivePokemon, otherTeam, otherTeamActivePokemon, text, team, turnNum):
    battle = template.copy()

    # Add Pokemon
    p1 = "Images/firered-leafgreen/back/"+str(currentTeam[currentTeamActivePokemon].id)+".PNG"
    battle = overlayImage(battle, p1, 115, 195, mult=1.5)
    p2 = "Images/firered-leafgreen/front/"+str(otherTeam[otherTeamActivePokemon].id)+".PNG"
    battle = overlayImage(battle, p2, 525, 95, mult=1.1)

    # add bottom
    x_offset = 0
    y_offset = 420
    battle[y_offset:y_offset+b.shape[0], x_offset:x_offset+b.shape[1]] = b


    # Add information on what happened
    cv.putText(battle, "Turn "+str(turnNum)+":", (20, 470), fontScale=1, color=(255, 255, 255), thickness=2,
               fontFace=cv.FONT_HERSHEY_DUPLEX)
    temp = text.split()
    yMod = 0
    while len(temp) > 0:
        t = ""
        while len(t) < 40 and len(temp) > 0:
            t += temp.pop(0)+" "
        cv.putText(battle, t, (20, 510+yMod), fontScale=1, color=(255, 255, 255), thickness=2,
                   fontFace=cv.FONT_HERSHEY_DUPLEX)
        yMod += 40

    # Status conditions
    xMod = 0
    for sc in otherTeam[otherTeamActivePokemon].statusEffects:
        p = "Images/Status Conditions/"+str(int(sc))+".png"
        if os.path.isfile(p):
            battle = overlayImage(battle, p, 495+xMod, 91, 1)
            xMod += 40
    xMod = 0
    for sc in currentTeam[currentTeamActivePokemon].statusEffects:
        p = "Images/Status Conditions/"+str(int(sc))+".png"
        if os.path.isfile(p):
            battle = overlayImage(battle, p, 125+xMod, 188, 1)
            xMod += 40

    # Add Name / Level
    t = str(currentTeam[currentTeamActivePokemon].name).capitalize()+" - L"+str(
        currentTeam[currentTeamActivePokemon].level)
    cv.putText(battle, t, (130, 150), fontScale=0.75, color=(0, 0, 0), thickness=4,
               fontFace=cv.FONT_HERSHEY_DUPLEX)
    cv.putText(battle, t, (130, 150), fontScale=0.75, color=(255, 255, 255), thickness=1,
               fontFace=cv.FONT_HERSHEY_DUPLEX)

    t = str(otherTeam[otherTeamActivePokemon].name).capitalize()+" - L"+str(
        otherTeam[otherTeamActivePokemon].level)
    cv.putText(battle, t, (530, 55), fontScale=0.75, color=(0, 0, 0), thickness=4,
               fontFace=cv.FONT_HERSHEY_DUPLEX)
    cv.putText(battle, t, (530, 55), fontScale=0.75, color=(255, 255, 255), thickness=1,
               fontFace=cv.FONT_HERSHEY_DUPLEX)

    # Add Pokeballs / Party Pokemon
    ySpace = 0
    for p in currentTeam:
        t = 0
        g = False
        if p.seen:
            if p.hp <= 0:
                g = True
            pt = "Images/firered-leafgreen/front/"+str(p.id)+".PNG"
        else:
            pt = "Images/pokeball.png"
            t += 5
        battle = overlayImage(battle, pt, 10+t, 17+ySpace, mult=0.25, grey=g)
        ySpace += 70
    ySpace = 0
    for p in otherTeam:
        t = 0
        g = False
        if p.seen:
            if p.hp <= 0:
                g = True
            pt = "Images/firered-leafgreen/front/"+str(p.id)+".PNG"
        else:
            t += 5
            pt = "Images/pokeball.png"
        battle = overlayImage(battle, pt, 840+t, 17+ySpace, mult=0.25, grey=g)
        ySpace += 70

    # Add HP
    percentHealth = currentTeam[currentTeamActivePokemon].hp / currentTeam[currentTeamActivePokemon].maxHp
    battle = rounded_rectangle(battle, (117, 165), (182, 132+int(224 * percentHealth)), 1, color=(0, 225, 0),
                               thickness=-1)
    s = str(int(percentHealth * 100))
    cv.putText(battle, s.rjust(3)+"%", (360, 179), fontScale=0.5, color=(255, 255, 255), thickness=1,
               fontFace=cv.FONT_HERSHEY_DUPLEX)

    percentHealth = otherTeam[otherTeamActivePokemon].hp / otherTeam[otherTeamActivePokemon].maxHp
    battle = rounded_rectangle(battle, (534, 70), (85, 550+int(224 * percentHealth)), 1, color=(0, 225, 0),
                               thickness=-1)
    s = str(int(percentHealth * 100))
    cv.putText(battle, s.rjust(3)+"%", (488, 82), fontScale=0.5, color=(255, 255, 255), thickness=1,
               fontFace=cv.FONT_HERSHEY_DUPLEX)

    # Turn Num and Current Team
    s = "TEAM "+str(team)
    cv.putText(battle, s, (90, 49), fontScale=1, color=(255, 255, 255), thickness=2,
               fontFace=cv.FONT_HERSHEY_DUPLEX)

    if team == 1:
        cv.imshow("BattleTeam1", battle)
    elif team == 2:
        cv.imshow("BattleTeam2", battle)


def displayWinner(win):
    battle = template.copy()
    cv.rectangle(battle, (50, 50), (850, 550), (255, 255, 255), thickness=-1)
    cv.putText(battle, "TEAM "+str(win)+" IS THE WINNER", (70, 300), fontScale=2, color=(0, 0, 0), thickness=7,
               fontFace=cv.FONT_HERSHEY_DUPLEX)
    cv.imshow("BattleTeam1", battle)
    cv.imshow("BattleTeam2", battle)
    cv.waitKey(0)


def rounded_rectangle(src, top_left, bottom_right, radius=1, color=(255, 255, 255), thickness=-1, line_type=cv.LINE_AA):
    p1 = top_left
    p2 = (bottom_right[1], top_left[1])
    p3 = (bottom_right[1], bottom_right[0])
    p4 = (top_left[0], bottom_right[0])

    height = abs(bottom_right[0]-top_left[1])

    if radius > 1:
        radius = 1

    corner_radius = int(radius * (height / 2))

    if thickness < 0:
        # big rect
        top_left_main_rect = (int(p1[0]+corner_radius), int(p1[1]))
        bottom_right_main_rect = (int(p3[0]-corner_radius), int(p3[1]))

        top_left_rect_left = (p1[0], p1[1]+corner_radius)
        bottom_right_rect_left = (p4[0]+corner_radius, p4[1]-corner_radius)

        top_left_rect_right = (p2[0]-corner_radius, p2[1]+corner_radius)
        bottom_right_rect_right = (p3[0], p3[1]-corner_radius)

        all_rects = [
            [top_left_main_rect, bottom_right_main_rect],
            [top_left_rect_left, bottom_right_rect_left],
            [top_left_rect_right, bottom_right_rect_right]]

        [cv.rectangle(src, rect[0], rect[1], color, thickness) for rect in all_rects]

    # draw straight lines
    cv.line(src, (p1[0]+corner_radius, p1[1]), (p2[0]-corner_radius, p2[1]), color, abs(thickness), line_type)
    cv.line(src, (p2[0], p2[1]+corner_radius), (p3[0], p3[1]-corner_radius), color, abs(thickness), line_type)
    cv.line(src, (p3[0]-corner_radius, p4[1]), (p4[0]+corner_radius, p3[1]), color, abs(thickness), line_type)
    cv.line(src, (p4[0], p4[1]-corner_radius), (p1[0], p1[1]+corner_radius), color, abs(thickness), line_type)

    # draw arcs
    cv.ellipse(src, (p1[0]+corner_radius, p1[1]+corner_radius), (corner_radius, corner_radius), 180.0, 0, 90, color,
               thickness, line_type)
    cv.ellipse(src, (p2[0]-corner_radius, p2[1]+corner_radius), (corner_radius, corner_radius), 270.0, 0, 90, color,
               thickness, line_type)
    cv.ellipse(src, (p3[0]-corner_radius, p3[1]-corner_radius), (corner_radius, corner_radius), 0.0, 0, 90, color,
               thickness, line_type)
    cv.ellipse(src, (p4[0]+corner_radius, p4[1]-corner_radius), (corner_radius, corner_radius), 90.0, 0, 90, color,
               thickness, line_type)

    return src
