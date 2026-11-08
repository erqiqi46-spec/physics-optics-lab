import {test,expect} from '@playwright/test';
test('光路随物体移动、焦点平行与虚像延长线实时切换',async({page})=>{
 await page.goto('/');await expect(page.getByTestId('ray-diagram')).toBeVisible();const line=page.locator('[data-ray="central-out"]');const before=await line.getAttribute('y2');await page.getByRole('spinbutton',{name:'发光物体位置数值'}).fill('20');await expect(line).not.toHaveAttribute('y2',before!);
 await page.getByRole('spinbutton',{name:'发光物体位置数值'}).fill('30');await expect(page.locator('.diagram-heading')).toContainText('出射光互相平行');expect(await page.locator('[data-ray$="-virtual"]').count()).toBe(0);
 await page.getByRole('spinbutton',{name:'发光物体位置数值'}).fill('35');await expect(page.locator('[data-ray="central-virtual"]')).toHaveAttribute('stroke-dasharray','6 5');await expect(page.getByTestId('screen-status')).toContainText('无法承接');
 await page.getByRole('button',{name:'光线已显示',exact:true}).click();await expect(page.getByTestId('ray-diagram')).toHaveCount(0);await page.getByRole('button',{name:'显示实时光路'}).click();await expect(page.getByTestId('ray-diagram')).toBeVisible();await page.screenshot({path:'evidence/06-live-rays-virtual.png',fullPage:true});
});
test('十五道易错题、解析、错题复习、进度保留与弹窗层级',async({page})=>{
 await page.goto('/');await page.getByRole('button',{name:'实验总结与自测'}).click();const modal=page.getByRole('dialog');await expect(modal.getByRole('button',{name:/^第\d+题$/})).toHaveCount(15);
 const correct=[1,2,1,1,2,2,1,1,0,1,1,1,1,0,2];
 for(let i=0;i<15;i++){await modal.getByRole('button',{name:`第${i+1}题`,exact:true}).click();await modal.locator('.quiz-options button').nth(i===0?0:correct[i]).click();await expect(modal.locator('.quiz-explanation')).toContainText(i===0?'这道题答错了':'回答正确');await expect(modal.locator('.common-mistake')).toContainText('易错：');if(i===0)await expect(modal.locator('.feedback')).not.toContainText('回答正确');}
 await expect(modal.locator('.quiz-complete')).toContainText('14/15');await modal.getByRole('button',{name:'只看错题',exact:true}).click();await expect(modal.getByRole('button',{name:/^第\d+题$/})).toHaveCount(1);await expect(modal.getByTestId('question-prompt')).toContainText('焦点以内');
 await modal.getByRole('button',{name:'去实验中观察此情境'}).click();await expect(modal).toBeHidden();await expect(page.getByTestId('screen-status')).toContainText('无法承接');await page.getByRole('button',{name:'实验总结与自测'}).click();await expect(modal.locator('.quiz-score')).toContainText('15/15');
 const block=await modal.boundingBox();expect(await page.evaluate(({x,y})=>!!document.elementFromPoint(x,y)?.closest('.modal'),{x:block!.x+35,y:block!.y+120})).toBe(true);await modal.screenshot({path:'evidence/07-mistake-review.png'});await modal.getByRole('button',{name:'重新作答'}).click();await modal.locator('.quiz-options button').nth(1).click();await expect(modal.locator('.feedback')).toContainText('回答正确');await page.keyboard.press('Escape');await expect(modal).toBeHidden();
});
